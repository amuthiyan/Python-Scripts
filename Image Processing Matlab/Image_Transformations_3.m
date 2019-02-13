%3.1
%b)
duck = imread('duck.jpg');
duck = double(duck);
nrows = size(duck,1);
ncols = size(duck,2);
[X,Y] = meshgrid(1:ncols,1:nrows);
X = reshape(X,50589,1);
Y = reshape(Y,50589,1);
R = duck(:,:,1); 
G = duck(:,:,2); 
B = duck(:,:,3); 
R = R(:);
G = G(:);
B = B(:);
R = normalize(R,'range');
G = normalize(G,'range');
B = normalize(B,'range');
X = normalize(X,'range');
Y = normalize(Y,'range');
F = cat(2,R,G,B,X,Y);
disp(size(F));
%disp(R);
F_kmeans = kmeans(F,2);
%disp(F_kmeans);
figure;
imshowpair(duck,F_kmeans,'montage');

%3.2
%c)
coins = imread('coins.png');
coins_thresh = im2bw(coins,0.35);


stats = regionprops('table',coins_thresh,'Centroid','MajorAxisLength','MinorAxisLength');
centers = stats.Centroid;
radii = (mean([stats.MajorAxisLength stats.MinorAxisLength],2))/2;

figure;
imshow(coins_thresh);
hold on
viscircles(centers,radii);
hold off

%3.3
%c)
cameraman = imread('cameraman.tif');
se = strel('square',3);
cameraman_dil = imdilate(cameraman,se);

cameraman_er = imerode(cameraman,se);

basic_grad = cameraman_dil - cameraman_er;

ex_grad = cameraman_dil - cameraman;

in_grad = cameraman - cameraman_er;

figure;
subplot(2,3,1);
imshow(cameraman);
subplot(2,3,2);
imshow(cameraman_dil);
subplot(2,3,3);
imshow(cameraman_er);
subplot(2,3,4);
imshow(basic_grad);
subplot(2,3,5);
imshow(ex_grad);
subplot(2,3,6);
imshow(in_grad);

%3.4)
%b)
Im = [[0 0 0 1 1 1 0 0];
      [1 1 1 1 1 1 0 0];
      [1 1 1 1 1 1 1 1];
      [1 1 1 1 1 1 1 1];
      [1 1 1 1 1 1 1 1];
      [1 1 1 1 1 1 1 0]];
  
Im = padarray(Im,[1 1],0,'both');
Im2 = Im;

for i = 2: size(Im2,1)-1
    for j = 2: size(Im2,2)-1
        if (Im(i,j)==0)
            Im2(i,j) = Im(i,j);
        else
            %Im2(i,j) = Im2(i,j) + 1;
            c1 = min(Im2(i,j-1),Im2(i-1,j));
            c2 = min(Im2(i-1,j-1),Im2(i-1,j+1));
            Im2(i,j) = min(c1,c2)+1;
        end
    end
end
Im3 = Im2;
for i = size(Im3,1)-1:-1:2 
    for j = size(Im3,2)-1:-1:2 
        %if (Im3(i+1,j) == 0 || Im3(i,j+1) == 0 || Im3(i+1,j-1) == 0 || Im3(i+1,j+1) == 0)
        if(Im3(i,j)==0)
            Im3(i,j) = Im3(i,j);
        else
            Im3(i,j) = (min(Im3(i,j),Im2(i,j)))+1;
            c1 = min(Im3(i,j+1),Im3(i+1,j));
            c2 = min(Im3(i+1,j-1),Im3(i+1,j+1));
            Im3(i,j) = min(Im2(i,j),min(c1,c2)+1);
        end
    end
end

disp(Im2);
disp(Im3);


Im2 = Im;

for i = 2: size(Im2,1)-1
    for j = 2: size(Im2,2)-1
        if (Im2(i,j)==0)
            Im2(i,j) = Im2(i,j);
        else
            %Im2(i,j) = Im2(i,j) + 1;
            Im2(i,j) = min(Im2(i,j-1),Im2(i-1,j))+1;
        end
    end
end
Im3 = Im2;
for i = size(Im3,1)-1:-1:2 
    for j = size(Im3,1)-1:-1:2 
        if (Im3(i,j) == 0)
            Im3(i,j) = Im3(i,j);
        else
            Im3(i,j) = min(Im2(i,j),min(Im3(i+1,j),Im3(i,j+1))+1);
        end
    end
end

disp(Im2);
disp(Im3);


%disp(base_com);

%3.5)
%b)
coins = imread('coins.png');
level = graythresh(coins);
coins_bw = imbinarize(coins,level);

figure;
imshowpair(coins,coins_bw,'montage');

disp(level);