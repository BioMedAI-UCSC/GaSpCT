#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
import torch.nn.functional as F
from torch.autograd import Variable
from math import exp
from scipy.special import gamma, gammaln

def l1_loss(network_output, gt):
    return torch.abs((network_output - gt)).mean()

def l2_loss(network_output, gt):
    return ((network_output - gt) ** 2).mean()

def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2)) for x in range(window_size)])
    return gauss / gauss.sum()

def create_window(window_size, channel):
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())
    return window

# For now, TV loss assumes RGB images, to be changed to grayscale
# TODO: test the function before merging
def tv_loss(img):
    tv_loss = 0
    img_norm = img  / 255.0
    # Calculate vertical pixel differences
    img_diff_v = img_norm[:-1, :, :] - img_norm[1:, :, :]
    tv_loss += torch.sum(torch.abs(img_diff_v))
    # Calculate horizontal pixel differences
    img_diff_h = img_norm[:, :-1, :] - img_norm[:, 1:, :] 
    tv_loss += torch.sum(torch.abs(img_diff_h))
    tv_loss_norm = torch.mean(tv_loss)
    return tv_loss_norm

# For now, Beta distribution loss assumes RGB images, to be changed to grayscale
def beta_loss(img, alpha=0.5, beta=0.5):

  # Clamp image values to valid domain
  img = torch.clamp(img, 1e-5, 1 - 1e-5) 
  
  img_alpha = img
  img_beta = 1 - img

  # Parameters
  a = torch.tensor(alpha)
  b = torch.tensor(beta)

  # Gamma functions
  g_a = gamma(a)
  g_b = gamma(b)
  g_ab = gamma(a + b)
  
  # Log gamma functions
  log_g_a = gammaln(a) 
  log_g_b = gammaln(b)
  log_g_ab = gammaln(a + b)

  # Calculate beta loss
  loss = -log_g_ab + log_g_a + log_g_b - (a-1)*torch.log(img_alpha) - (b-1)*torch.log(img_beta)

  return torch.mean(loss)


def ssim(img1, img2, window_size=11, size_average=True):
    channel = img1.size(-3)
    window = create_window(window_size, channel)

    if img1.is_cuda:
        window = window.cuda(img1.get_device())
    window = window.type_as(img1)

    return _ssim(img1, img2, window, window_size, channel, size_average)

def _ssim(img1, img2, window, window_size, channel, size_average=True):
    mu1 = F.conv2d(img1, window, padding=window_size // 2, groups=channel)
    mu2 = F.conv2d(img2, window, padding=window_size // 2, groups=channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2

    sigma1_sq = F.conv2d(img1 * img1, window, padding=window_size // 2, groups=channel) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=window_size // 2, groups=channel) - mu2_sq
    sigma12 = F.conv2d(img1 * img2, window, padding=window_size // 2, groups=channel) - mu1_mu2

    C1 = 0.01 ** 2
    C2 = 0.03 ** 2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    if size_average:
        return ssim_map.mean()
    else:
        return ssim_map.mean(1).mean(1).mean(1)

