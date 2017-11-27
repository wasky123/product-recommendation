clear; close all; clc

addpath('G:\graduate\uf\2017fall\class\cloud comp and store\project\create\ae\auto_results');

load('matrix.mat');
train_x = matrix;

%% normalization
train_x = train_x./5;

%%  ex1 train a 100 hidden unit SDAE and use it to initialize a FFNN
%  Setup and train a stacked denoising autoencoder (SDAE)

sae = saesetup([10554 1000]);
%% parameter in first layer
sae.ae{1}.activation_function       = 'sigm';
sae.ae{1}.learningRate              = 0.9;
sae.ae{1}.nn.weightPenaltyL2   = 0.1;
sae.ae{1}.dropoutFraction = 0;

opts.numepochs =  10;
opts.batchsize = 100;
sae = saetrain(sae, train_x, opts);

m = size(train_x,1);

%% feedforward
wi_h = sae.ae{1,1}.W{1,1}';% 3682*500
wh_o = sae.ae{1,1}.W{1,2}'; % 501*3681
inp_value = [ones(m,1),train_x]; % 6040*3682
hid_value = [ones(m,1),sigm(inp_value * wi_h)];% 6040*3682 * 3682*500 + 1 -> 6040*501
out_value = sigm(hid_value * wh_o);% 6040*501 * 501*3681
visualize(sae.ae{1}.W{1}(:,2:end)')
tem = out_value;
tem(tem<=1e-4)=0;
y = tem.*10;
figure;imshow(y);
figure;imshow(train_x);
save('result.mat','tem')

% % Use the SDAE to initialize a FFNN
% nn = nnsetup([784 100 10]);
% nn.activation_function              = 'sigm';
% nn.learningRate                     = 1;
% nn.W{1} = sae.ae{1}.W{1};
% 
% % Train the FFNN
% opts.numepochs =   1;
% opts.batchsize = 100;
% nn = nntrain(nn, train_x, train_y, opts);
% [er, bad] = nntest(nn, test_x, test_y);
% assert(er < 0.16, 'Too big error');
% 
% %% ex2 train a 100-100 hidden unit SDAE and use it to initialize a FFNN
% %  Setup and train a stacked denoising autoencoder (SDAE)
% rand('state',0)
% sae = saesetup([784 100 100]);
% sae.ae{1}.activation_function       = 'sigm';
% sae.ae{1}.learningRate              = 1;
% sae.ae{1}.inputZeroMaskedFraction   = 0.5;
% 
% sae.ae{2}.activation_function       = 'sigm';
% sae.ae{2}.learningRate              = 1;
% sae.ae{2}.inputZeroMaskedFraction   = 0.5;
% 
% opts.numepochs =   1;
% opts.batchsize = 100;
% sae = saetrain(sae, train_x, opts);
% visualize(sae.ae{1}.W{1}(:,2:end)')
% 
% % Use the SDAE to initialize a FFNN
% nn = nnsetup([784 100 100 10]);
% nn.activation_function              = 'sigm';
% nn.learningRate                     = 1;
% 
% %add pretrained weights
% nn.W{1} = sae.ae{1}.W{1};
% nn.W{2} = sae.ae{2}.W{1};
% 
% % Train the FFNN
% opts.numepochs =   1;
% opts.batchsize = 100;
% nn = nntrain(nn, train_x, train_y, opts);
% [er, bad] = nntest(nn, test_x, test_y);
% assert(er < 0.1, 'Too big error');
