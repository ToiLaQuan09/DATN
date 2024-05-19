# import av
# import os
# import sys
# import streamlit as st
# import cv2
# import tempfile


# BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
# sys.path.append(BASE_DIR)


# from utils_draw import get_mediapipe_pose
# from process_frame import ProcessFrame
# from thresholds import get_thresholds_beginner, get_thresholds_pro



# st.title(f'Mô hình đánh giá tư thế thể dục Squat')

# mode_all = st.radio(f'Chọn chế độ chiếu', ['Trực tiếp', 'Video'])
# mode = st.radio(f'Chọn chế độ', ['Mới bắt đầu', 'Đã thành thạo'], horizontal=True)

# thresholds = None 

# if mode == 'Mới bắt đầu':
#     thresholds = get_thresholds_beginner()

# elif mode == 'Đã thành thạo':
#     thresholds = get_thresholds_pro()



# upload_process_frame = ProcessFrame(thresholds=thresholds)

# # Initialize face mesh solution
# pose = get_mediapipe_pose()


# download = None

# if 'download' not in st.session_state:
#     st.session_state['download'] = False


# output_video_file = f'output_recorded.mp4'

# if os.path.exists(output_video_file):
#     os.remove(output_video_file)


# with st.form('Upload', clear_on_submit=True):
#     up_file = st.file_uploader("Upload a Video", ['mp4','mov', 'avi'])
#     uploaded = st.form_submit_button("Upload")

# stframe = st.empty()

# ip_vid_str = '<p style="font-family:Helvetica; font-weight: bold; font-size: 16px;">Input Video</p>'
# warning_str = '<p style="font-family:Helvetica; font-weight: bold; color: Red; font-size: 17px;">Please Upload a Video first!!!</p>'

# warn = st.empty()


# download_button = st.empty()

# if up_file and uploaded:
    
#     download_button.empty()
#     tfile = tempfile.NamedTemporaryFile(delete=False)

#     try:
#         warn.empty()
#         tfile.write(up_file.read())

#         vf = cv2.VideoCapture(tfile.name)

#         # ---------------------  Write the processed video frame. --------------------
#         fps = int(vf.get(cv2.CAP_PROP_FPS))
#         width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         frame_size = (width, height)
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         video_output = cv2.VideoWriter(output_video_file, fourcc, fps, frame_size)
#         # -----------------------------------------------------------------------------

        
#         txt = st.sidebar.markdown(ip_vid_str, unsafe_allow_html=True)   
#         ip_video = st.sidebar.video(tfile.name) 

#         while vf.isOpened():
#             ret, frame = vf.read()
#             if not ret:
#                 break

#             # convert frame from BGR to RGB before processing it.
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             out_frame, _ = upload_process_frame.process(frame, pose)
#             stframe.image(out_frame)
#             video_output.write(out_frame[...,::-1])

        
#         vf.release()
#         video_output.release()
#         stframe.empty()
#         ip_video.empty()
#         txt.empty()
#         tfile.close()
    
#     except AttributeError:
#         warn.markdown(warning_str, unsafe_allow_html=True)   



# if os.path.exists(output_video_file):
#     with open(output_video_file, 'rb') as op_vid:
#         download = download_button.download_button('Download Video', data = op_vid, file_name='output_recorded.mp4')
    
#     if download:
#         st.session_state['download'] = True



# if os.path.exists(output_video_file) and st.session_state['download']:
#     os.remove(output_video_file)
#     st.session_state['download'] = False
#     download_button.empty()


import av
import os
import sys
import streamlit as st
import cv2
import tempfile
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder

# Thiết lập đường dẫn
BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)

# Import các module tự tạo
from utils_draw import get_mediapipe_pose
from process_frame import ProcessFrame
from thresholds import get_thresholds_beginner, get_thresholds_pro

st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
# Tiêu đề ứng dụng
st.title(f'ĐÁNH GIÁ TƯ THẾ THỂ DỤC SQUAT')

# Chọn chế độ chiếu
st.markdown('<p class="big-font">Chọn chế độ trình chiếu</p>', unsafe_allow_html=True)
mode_all = st.selectbox('', ['Trực tiếp', 'Video'],index=None, placeholder='Chọn chế độ...')
st.write('Bạn đã chọn: ', mode_all)
# Chọn chế độ
st.markdown('<p class="big-font">Chọn chế độ tập luyện</p>', unsafe_allow_html=True)
mode = st.selectbox('', ('Mới bắt đầu', 'Đã thành thạo'), index=None, placeholder='Chọn chế độ...')
st.write('Bạn đã chọn: ', mode)
# Lấy ngưỡng cho chế độ
thresholds = None
if mode == 'Mới bắt đầu':
    thresholds = get_thresholds_beginner()
elif mode == 'Đã thành thạo':
    thresholds = get_thresholds_pro()

# Tạo đối tượng xử lý khung hình


# Khởi tạo Mediapipe pose
pose = get_mediapipe_pose()

# Kiểm tra trạng thái tải về
if 'download' not in st.session_state:
    st.session_state['download'] = False

# Tên file đầu ra
output_video_file = 'output_recorded.mp4'

# Xóa file nếu đã tồn tại
if os.path.exists(output_video_file):
    os.remove(output_video_file)

# Xử lý video upload
if mode_all == 'Video':
    upload_process_frame = ProcessFrame(thresholds=thresholds)

    with st.form('Upload', clear_on_submit=True):
        up_file = st.file_uploader("Upload a Video", ['mp4','mov', 'avi'])
        uploaded = st.form_submit_button("Upload")

    stframe = st.empty()

    ip_vid_str = '<p style="font-family:Helvetica; font-weight: bold; font-size: 16px;">Input Video</p>'
    warning_str = '<p style="font-family:Helvetica; font-weight: bold; color: Red; font-size: 17px;">Please Upload a Video first!!!</p>'
    warn = st.empty()
    download_button = st.empty()

    if up_file and uploaded:
        download_button.empty()
        tfile = tempfile.NamedTemporaryFile(delete=False)

        try:
            warn.empty()
            tfile.write(up_file.read())
            vf = cv2.VideoCapture(tfile.name)

            # Khởi tạo đối tượng ghi video
            fps = int(vf.get(cv2.CAP_PROP_FPS))
            width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_size = (width, height)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_output = cv2.VideoWriter(output_video_file, fourcc, fps, frame_size)

            # Hiển thị video đầu vào
            txt = st.sidebar.markdown(ip_vid_str, unsafe_allow_html=True)
            ip_video = st.sidebar.video(tfile.name)

            # Xử lý từng khung hình
            while vf.isOpened():
                ret, frame = vf.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out_frame, _ = upload_process_frame.process(frame, pose)
                stframe.image(out_frame)
                video_output.write(out_frame[...,::-1])

            vf.release()
            video_output.release()
            stframe.empty()
            ip_video.empty()
            txt.empty()
            tfile.close()

        except AttributeError:
            warn.markdown(warning_str, unsafe_allow_html=True)

    if os.path.exists(output_video_file):
        with open(output_video_file, 'rb') as op_vid:
            download = download_button.download_button('Download Video', data=op_vid, file_name='output_recorded.mp4')
            if download:
                st.session_state['download'] = True

    if os.path.exists(output_video_file) and st.session_state['download']:
        os.remove(output_video_file)
        st.session_state['download'] = False
        download_button.empty()

# Xử lý livestream
elif mode_all == 'Trực tiếp':
    live_process_frame = ProcessFrame(thresholds=thresholds, flip_frame=True)

    output_video_file = 'output_live.flv'

    def video_frame_callback(frame: av.VideoFrame):
        frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
        frame, _ = live_process_frame.process(frame, pose)  # Process frame
        return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return RGB frame

    def out_recorder_factory() -> MediaRecorder:
        return MediaRecorder(output_video_file)

    ctx = webrtc_streamer(
        key="Squats-pose-analysis",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
        media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
        out_recorder_factory=out_recorder_factory
    )

    download_button = st.empty()

    if os.path.exists(output_video_file):
        with open(output_video_file, 'rb') as op_vid:
            download = download_button.download_button('Download Video', data=op_vid, file_name='output_live.flv')
            if download:
                st.session_state['download'] = True

    if os.path.exists(output_video_file) and st.session_state['download']:
        os.remove(output_video_file)
        st.session_state['download'] = False
        download_button.empty()

    
    

    


