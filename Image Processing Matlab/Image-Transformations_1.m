%1.1
barbara = imread('barbara.jpg');
imshow(barbara);

imwrite(barbara,'barbara_mine.jpg');
barbara_mine = imread('barbara_mine.jpg');
imshow(barbara_mine);

%1.2
img_gray = rgb2gray(barbara);
imshow(img_gray);

imwrite(img_gray,'barbara_gray.png');
img_gray_double = im2double(img_gray);
imshow(img_gray_double);


%1.3
%a)
F = imread('Lena.jpg');
Lena_crop = imcrop(F,[170 170 170 170]);
imshow(Lena_crop);

%b)
Lenaplus100 = imadd(Lena_crop,100);
imshow(Lenaplus100);

%c)
Lena_Mul = Lena_crop*2;
imshow(Lena_Mul);

Lena_Div = Lena_crop/2;
imshow(Lena_Div);

%d)
camera_man = imread('cameraman.jpg');
camera_man_crop = imcrop(camera_man,[1,1,170,170]);
imshow(camera_man_crop);

combined = imadd(Lena_crop,camera_man_crop);
imshow(combined);

%1.4
%a)
lena_bmp = imread('lena_256.bmp');
lena_bmp_double = double(lena_bmp);
imshow(lena_bmp_double);

lena_thresholded = lena_bmp_double;
lena_thresholded(lena_bmp_double<100) = 1;
lena_thresholded(lena_bmp_double>200) = 1;
lena_thresholded(lena_thresholded~=1) = 0;
imshow(lena_thresholded);

%b)
level = graythresh(lena_bmp);
lena_otsu = imbinarize(lena_bmp,level);
imshowpair(lena_bmp,lena_otsu,'montage');

%c)
lena_down = imresize(lena_bmp,[64 64]);
imshow(lena_down);

lena_up = imresize(lena_down,[256 256]);
imshow(lena_up);

%d)
lena_gray = rgb2gray(lena_bmp);
mask = ones(3);
mask = mask*(1/9);
lena_conv_3 = conv2(lena_gray,mask);
imshow(lena_conv_3,[]);

mask_5 = ones(5);
mask_5 = mask_5*(1/25);
lena_conv_5 = convn(lena_gray,mask_5);
imshow(lena_conv_5,[]);