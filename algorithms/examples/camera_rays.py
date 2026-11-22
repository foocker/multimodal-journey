"""相机射线与 Plücker 条件；R为camera→world，尺度与坐标由调用者保证。"""
import torch


def plucker_rays(pixel_homogeneous, intrinsics, rotation, camera_center):
    camera_dirs = torch.linalg.solve(intrinsics, pixel_homogeneous.reshape(-1, 3).T).T
    directions = camera_dirs @ rotation.T
    directions = directions / directions.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    moments = torch.linalg.cross(camera_center.expand_as(directions), directions)
    return torch.cat((directions, moments), dim=-1).reshape(*pixel_homogeneous.shape[:-1], 6)
