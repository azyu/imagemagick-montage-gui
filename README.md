# 설명

여러 사진을 한 장의 격자 사진으로 합쳐주는 프로그램입니다. (JPG 또는 PNG 형식으로 저장됩니다.)

내부적으로 [ImageMagick](https://imagemagick.org)의 [montage](https://imagemagick.org/script/montage.php)를 사용합니다.

![image](https://github.com/azyu/imagemagick-montage-gui/assets/1789839/ec62f96f-d89a-4e1d-88a1-91c71182c64e)
![image](https://github.com/azyu/imagemagick-montage-gui/assets/1789839/f009b8a0-8307-4fc4-95d1-798bb07956e9)

# 사전 준비 사항

Windows 사용자는 [이 페이지에 있는 Windows Binary Release](https://imagemagick.org/script/download.php#windows) 페이지에 있는 아래 파일을 다운로드 받아서 설치해주세요.

```
ImageMagick-x.x.x-xx-Q16-HDRI-x64-dll.exe
```

<img alt="image" src="https://github.com/azyu/imagemagick-montage-gui/assets/1789839/d1544ff2-7147-41ca-b537-625a3d09a66a">

# 사용법
1. [Release](https://github.com/azyu/imagemagick-montage-gui/releases) 페이지에 가셔서 magick-montage-gui.Windows.zip 파일을 다운로드 받습니다.
2. 압축을 해제하고 magick-montage-gui.exe 파일을 실행합니다.
3. 왼쪽 패널의 [사진 파일 추가] 버튼을 눌러서 합치고자 하는 사진 파일을 골라주세요. 한 번에 여러 장 선택도 가능합니다.
4. 추가한 사진 숫자에 맞게 오른쪽 패널의 행과 열을 수정해주세요. 예를 들어 사진 파일이 8장이라면 행 4/열 2 또는 열 2/행 4로 설정해주셔야 합니다.
5. 저장하기 버튼을 눌러 완성!
