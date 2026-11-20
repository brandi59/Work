import numpy as np, cv2, onnxruntime as ort
class Lama:
    def __init__(s,p,threads=4):
        o=ort.SessionOptions(); o.intra_op_num_threads=threads; o.inter_op_num_threads=1
        s.s=ort.InferenceSession(p,o)
    def fill(s,img,mask):
        """img BGR uint8 HxW (any size), mask uint8 HxW -> inpainted BGR resized back"""
        h,w=mask.shape; im=cv2.resize(img,(512,512),interpolation=cv2.INTER_AREA); m=cv2.resize(mask,(512,512),interpolation=cv2.INTER_NEAREST)
        x=im[...,::-1].transpose(2,0,1)[None].astype(np.float32)/255; mm=(m>127).astype(np.float32)[None,None]
        out=s.s.run(None,{'image':x,'mask':mm})[0][0].transpose(1,2,0)
        if out.max()<=1.5: out=out*255
        out=np.clip(out,0,255).astype(np.uint8)[...,::-1]
        return cv2.resize(out,(w,h),interpolation=cv2.INTER_CUBIC) if (w,h)!=(512,512) else out
