%4.4)
watermark = imread('njit_logo.jpg');
lena = imread('lena_256.bmp');

watermark = imresize(watermark,[100 130]);

watermark_bin = im2bw(watermark);



[num_rows, num_cols, num_channels] = size(watermark_bin);
disp(num_rows);
disp(num_cols);

bits = [1 3 5 7];
figure;
for i = 1:length(bits)
    watermarked_lena = lena;
    disp(bits(i));
    for column = 1:num_cols
        for row = 1:num_rows
            watermarked_lena(row,column) = bitset(lena(row,column),bits(i),watermark_bin(row,column));
        end
    end
    subplot(4,4,i);
    imshow(watermarked_lena);
    
    retrieved_mark = zeros(num_rows,num_cols);
    for column = 1:num_cols
        for row = 1:num_rows
            retrieved_mark(row,column) = bitget(watermarked_lena(row,column),bits(i));
        end
    end
    subplot(4,4,i+4);
    imshow(retrieved_mark);
    
    
    avgd_mark = conv2(rgb2gray(watermarked_lena), ones(3)/9, 'same');

    subplot(4,4,i+8);
    imshow(avgd_mark, []);
    
    avgd_mark = int8(avgd_mark);
    
    retrieved_avg_mark = zeros(num_rows,num_cols);
    for column = 1:num_cols
        for row = 1:num_rows
            retrieved_avg_mark(row,column) = bitget(avgd_mark(row,column),bits(i));
        end
    end
    subplot(4,4,i+12);
    imshow(retrieved_avg_mark);
end

%Try again)
lin = imread('Lin.jpg');
watermark = imread('njit_logo.jpg');

watermark = im2bw(watermark);
watermark = 10*watermark;
lin_gray = rgb2gray(lin);
lin_dct = dct2(lin_gray);
lin_marked = lin_dct;

[num_rows, num_cols] = size(watermark);
for row = 1:num_rows
    for col = 1:num_cols
        lin_marked(row,col) = lin_dct(row,col)+watermark(row,col);
    end
end
figure;
lin_idct = idct2(lin_marked);
imshow(lin_idct,[]);
%4.5)
lin = imread('Lin.jpg');
watermark = imread('njit_logo.jpg');

disp(size(lin));
disp(size(watermark));

watermark = im2bw(watermark);
watermark = 10*watermark;

%watermark = dct2(watermark);
%lin_water = lin;

lin_r = lin(:,:,1);
lin_g = lin(:,:,2);
lin_b = lin(:,:,3);

new_lin_r = dct2(lin_r);
new_lin_g = dct2(lin_g);
new_lin_b = dct2(lin_b);

[num_rows, num_cols] = size(watermark);
for row = 1:num_rows
    for col = 1:num_cols
        new_lin_r(row,col) = new_lin_r(row,col)+watermark(row,col);
        new_lin_g(row,col) = new_lin_g(row,col)+watermark(row,col);
        new_lin_b(row,col) = new_lin_b(row,col)+watermark(row,col);
        %disp('hi');
    end
end


%lin_out = lin_water;

lin_out_r = idct2(new_lin_r); 
lin_out_g = idct2(new_lin_g); 
lin_out_b = idct2(new_lin_b); 

lin_out = cat(3,lin_out_r,lin_out_g,lin_out_b);

de_lin_r = lin_out(:,:,1);
de_lin_g = lin_out(:,:,2);
de_lin_b = lin_out(:,:,3);

de_lin_r = dct2(de_lin_r);
de_lin_g = dct2(de_lin_g);
de_lin_b = dct2(de_lin_b);

[num_rows, num_cols] = size(watermark);
for row = 1:num_rows
    for col = 1:num_cols
        de_lin_r(row,col) = de_lin_r(row,col)-watermark(row,col);
        de_lin_g(row,col) = de_lin_g(row,col)-watermark(row,col);
        de_lin_b(row,col) = de_lin_b(row,col)-watermark(row,col);
        %disp('hi');
    end
end

de_out_r = idct2(de_lin_r); 
de_out_g = idct2(de_lin_g); 
de_out_b = idct2(de_lin_b); 

de_out = cat(3,de_out_r,de_out_g,de_out_b);

disp(size(lin_out));
lin_out = uint8(lin_out);
de_out = uint8(de_out);
lin_diff = imabsdiff(lin,lin_out);

de_diff = imabsdiff(lin,de_out);

figure;
subplot(2,3,1);
imshow(lin);
subplot(2,3,2);
imshow(lin_out);
subplot(2,3,3);
imshow(lin_diff);
subplot(2,3,4);
imshow(de_out);
subplot(2,3,5);
imshow(de_diff);

%b)
noise_mark = imnoise(lin_out,'gaussian');
noise_r = noise_mark(:,:,1);
noise_g = noise_mark(:,:,2);
noise_b = noise_mark(:,:,3);

noise_r = dct2(noise_r);
noise_g = dct2(noise_g);
noise_b = dct2(noise_b);

[num_rows, num_cols] = size(watermark);
for row = 1:num_rows
    for col = 1:num_cols
        noise_r(row,col) = noise_r(row,col)-watermark(row,col);
        noise_g(row,col) = noise_g(row,col)-watermark(row,col);
        noise_b(row,col) = noise_b(row,col)-watermark(row,col);
        %disp('hi');
    end
end

noise_r = idct2(noise_r);
noise_g = idct2(noise_g);
noise_b = idct2(noise_b);

noise_out = cat(3,noise_r,noise_g,noise_b);

figure;
subplot(1,2,1);
imshow(noise_mark);
subplot(1,2,2);
imshow(noise_out);

