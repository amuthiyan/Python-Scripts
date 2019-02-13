%2.2)
%a)
lena_bmp = imread('lena_256.bmp');
lena_salt_pepper = imnoise(lena_bmp,'salt & pepper',0.65);

lena_gray = rgb2gray(lena_bmp);
mask = ones(3);
mask = mask*(1/9);
lena_conv_3 = conv2(lena_gray,mask);

lena_gray = rgb2gray(lena_bmp);
mask = ones(7);
mask = mask*(1/49);
lena_conv_7 = conv2(lena_gray,mask);

lena_med_fil_3 = medfilt2(lena_gray,[3,3]);
lena_med_fil_7 = medfilt2(lena_gray,[7,7]);

figure;
subplot(2,3,1);
imshow(lena_bmp);
subplot(2,3,2);
imshow(lena_salt_pepper);
subplot(2,3,3);
imshow(lena_conv_3,[]);
subplot(2,3,4);
imshow(lena_conv_7,[]);
subplot(2,3,5);
imshow(lena_med_fil_3);
subplot(2,3,6);
imshow(lena_med_fil_7);

%b)
barbara_gray = imread('barbara_gray.jpg');

%Need to swap halves here, will do that later
%barbara_trans = barbara_gray;
barbara_trans = ifftshift(barbara_gray,2);

barbara_rot_crop = imrotate(barbara_gray,30,'nearest','crop');
barbara_rot_loose = imrotate(barbara_gray,30,'nearest','loose');

[rows,columns,numberOfColorChannels] = size(barbara_gray);
disp(size(barbara_gray));
newHorizontal = 0.5*columns;
newVertical = 0.75*rows;
barbara_scale = imresize(barbara_gray,[newHorizontal,newVertical]);
disp(size(barbara_scale));

figure;
subplot(2,3,1);
imshow(barbara_gray);
subplot(2,3,2);
imshow(barbara_trans);
subplot(2,3,3);
imshow(barbara_rot_crop);
subplot(2,3,4);
imshow(barbara_rot_loose);
subplot(2,3,5);
imshow(barbara_scale);
%subplot(2,3,6,'replace');

%c)
tform = maketform('affine',[1,0.1,0; 0.2,1,0; 0,0,1]);
barbara_shear = imtransform(barbara_gray,tform);
figure;
imshow(barbara_shear);

%2.3)
%a)
lena_bmp = imread('lena_256.bmp');
lena_div = lena_bmp/4;

lena_histeq = histeq(lena_div);

figure;
subplot(2,2,1);
imshow(lena_div);
subplot(2,2,2);
imhist(lena_div);
subplot(2,2,3);
imshow(lena_histeq);
subplot(2,2,4);
imhist(lena_histeq);

%b)
lena_bmp = imread('lena_256.bmp');
lena_sharpened = imsharpen(lena_bmp);

lena_gray = rgb2gray(lena_bmp);

lena_edge = edge(lena_gray);

figure;
subplot(2,2,1);
imshow(lena_bmp);
subplot(2,2,2);
imshow(lena_sharpened);
subplot(2,2,3);
imshow(lena_edge);

%c)
[low_filter,high_filter] = getfilters(40);

cameraman = imread('cameraman.jpg');
 
cam_fft = fft2(cameraman);
cam_fft_low = cam_fft.*low_filter;
cam_fft_high = cam_fft.*high_filter;
 
cam_low_filt = ifft2(cam_fft_low);
cam_high_filt = ifft2(cam_fft_high);
figure;
subplot(2,1,1);
imshow(abs(cam_low_filt));
subplot(2,1,2);
imshow(abs(cam_high_filt));



%2.4)
%a)
lena_bmp = imread('lena_256.bmp');

lena_bmp_double = double(lena_bmp);
imshow(lena_bmp_double);

lena_quantized = lena_bmp_double;
lena_quantized((0<=lena_quantized)&(lena_quantized<=63)) = 0;
lena_quantized((64<=lena_quantized)&(lena_quantized<=127)) = 64;
lena_quantized((128<=lena_quantized)&(lena_quantized<=191)) = 128;
lena_quantized((192<=lena_quantized)&(lena_quantized<=255)) = 255;
figure;
imshow(lena_quantized);

%b)
lena_bmp = imread('lena_256.bmp');
lena_bmp = rgb2gray(lena_bmp);

b1 = bitget(lena_bmp,2);
b3 = bitget(lena_bmp,3);
b4 = bitget(lena_bmp,4);
b5 = bitget(lena_bmp,5);
b6 = bitget(lena_bmp,6);
b7 = bitget(lena_bmp,7);
b8 = bitget(lena_bmp,8);

figure;
subplot(4,2,1);
imshow(b1,[]);
subplot(4,2,2);
imshow(b2,[]);
subplot(4,2,3);
imshow(b3,[]);
subplot(4,2,4);
imshow(b4,[]);
subplot(4,2,5);
imshow(b5,[]);
subplot(4,2,6);
imshow(b6,[]);
subplot(4,2,7);
imshow(b7,[]);
subplot(4,2,8);
imshow(b8,[]);

%2.5)
%a)
back1 = imread('back1.jpg');
back2 = imread('back2.jpg');

back_diff = imabsdiff(back1,back2);
back_comp = imcomplement(back_diff);

figure;
subplot(2,2,1);
imshow(back1);
subplot(2,2,2);
imshow(back2);
subplot(2,2,3);
imshow(back_diff,[]);
subplot(2,2,4);
imshow(back_comp);

%b)
chng1 = imread('chng1.jpg');
chng2 = imread('chng2.jpg');

chng_diff = imabsdiff(chng1,chng2);
chng_comp = imcomplement(chng_diff);

figure;
subplot(2,2,1);
imshow(chng1);
subplot(2,2,2);
imshow(chng2);
subplot(2,2,3);
imshow(chng_diff);
subplot(2,2,4);
imshow(chng_comp);

%c)
lena_bmp = imread('lena_256.bmp');
lena_gray = rgb2gray(lena_bmp);

kernel_3 = fspecial('gaussian',[3 3],1);
kernel_10 = fspecial('gaussian',[10 10],3); %Sigma is 3 if variance is 9

lena_gauss_3 = imfilter(lena_gray,kernel_3)
lena_gauss_10 = imfilter(lena_gray,kernel_10)

lena_gray_minus_3 = imsubtract(lena_gray,lena_gauss_3);
lena_gray_minus_10 = imsubtract(lena_gray,lena_gauss_10);

lena_3_minus_10 = imsubtract(lena_gauss_3,lena_gauss_10);

figure;
subplot(2,2,1);
imshow(lena_bmp);
subplot(2,2,2);
imshow(lena_gray_minus_3);
subplot(2,2,3);
imshow(lena_gray_minus_10);
subplot(2,2,4);
imshow(lena_3_minus_10);


function [cL,cH] = getfilters(radius) 
% a helper function returns the low and high pass filter 
[x,y] = meshgrid(-128:127,-128:127); 
z = sqrt(x.^2+y.^2); 
cL = z < radius; 
cH = ~cL; 
end 



