import re

s = """
    9.log:07-29 16:24:20.050 I/[APP][Time](27331): Init using time: 47 ms, current time: 1406622260061 ms
    9.log:07-29 16:24:20.530 I/[APP][Time](27331): Open using time: 73 ms, current time: 1406622260542 ms
    9.log:07-29 16:24:20.800 I/[APP][Time](27331): Open complete using time: 341 ms, current time: 1406622260810 ms
    9.log:07-29 16:24:20.890 I/[APP][Time](27331): Run using time: 87 ms, current time: 1406622260898 ms
    9.log:07-29 16:24:20.890 I/VOLOG   (27331): 16:24:20.899 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 138, VR IsHandshakeVerified+
    9.log:07-29 16:24:20.890 I/VOLOG   (27331): 16:24:20.900 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 140, VR IsHandshakeVerified- 1
    9.log:07-29 16:24:20.890 I/VOLOG   (27331): 16:24:20.900 @@@VOLOG,   Info, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 336, VR SetVCASCommunicationHandlerSettings+ /data/data/com.visualon.AppUI/
    9.log:07-29 16:24:22.560 I/VOLOG   (27331): 16:24:22.576 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 338, VR SetVCASCommunicationHandlerSettings- 0
    9.log:07-29 16:24:26.610 I/VOLOG   (27331): 16:24:26.627 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 397, VR CheckVCASConnection+
    9.log:07-29 16:24:28.820 I/VOLOG   (27331): 16:24:28.832 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 399, VR CheckVCASConnection- 0
    9.log:07-29 16:24:28.870 I/VOLOG   (27331): 16:24:28.881 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 829, VR Decrypt+ 601600
    9.log:07-29 16:24:29.150 I/VOLOG   (27331): 16:24:29.165 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 831, VR Decrypt- 0 601600
    9.log:07-29 16:24:29.480 I/VOLOG   (27331): 16:24:29.488 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 829, VR Decrypt+ 492944
    9.log:07-29 16:24:29.580 I/VOLOG   (27331): 16:24:29.596 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 831, VR Decrypt- 0 492944
    9.log:07-29 16:24:29.680 I/VOLOG   (27331): 16:24:29.690 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 138, VR IsHandshakeVerified+
    9.log:07-29 16:24:29.680 I/VOLOG   (27331): 16:24:29.690 @@@VOLOG,    Run, 0A030000, 023AD530, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 140, VR IsHandshakeVerified- 1
    9.log:07-29 16:24:29.930 I/[APP][Time](27331): Buffer using time: 9029 ms, current time: 1406622269943 ms
    9.log:07-29 16:24:30.080 I/[APP][Time](27331): Open to render using time: 9628 ms, current time: 1406622270097 ms
    """

p1 = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsDeviceProvisioned+"
p2 = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsHandshakeVerified"

result1 = re.findall(p1, s)
result2 = re.findall(p2, s)

print result1
print result2
