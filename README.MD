# This code contains sources from [this repository](https://github.com/thohemp/6DRepNet).
## The test video is taken from [https://youtu.be/lzLm2e0Fztw?t=41](https://youtu.be/lzLm2e0Fztw?t=41)
## The test image taken from [300W-3D](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm)
## Start-up instructions
0. You should have **git** and **docker** installed
1. Clone repository:
```bash
git clone https://github.com/danclas/dev-dl-system-course.git
```
2. Go to the cloned directory
```bash
cd dev-dl-system-course
```
3. Build docker image (**while** in the dev-dl-system-course directory):
```bash
docker build -t sixdnet_app .
```
4. Run docker (**while** in the dev-dl-system-course directory):

_On Linux_
```bash
docker run -v ./:/app --shm-size 8G sixdnet_app
```

_On Windows_
```bash
docker run -v .\:/app --shm-size 8G sixdnet_app
```

The resulting video is located at the **path** ```./output.mp4```