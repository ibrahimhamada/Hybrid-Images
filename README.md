# Hybrid-Images
Hybrid Images: Mini Project 1 of the Computer Vision Course Offered in Spring 2022 @ Zewail City

The project is adopted from a similar course in Brown University.
In hybrid images, specific frequencies tend to dominate at particular distances. For instance, high frequencies dominate when the object is closer, while lower frequencies become more dominant when it is farther away. 

## Low-Pass Filter
By using a Gaussian blur, we can create a low-pass filtered equivalent of the image and demonstrate the effect of hybrid images as shown:

![dog](https://github.com/ibrahimhamada/Hybrid-Images/assets/58476343/8164f81c-ea79-43dd-9bcf-3463dccc3eb1)    ![results-low_frequencies](https://github.com/ibrahimhamada/Hybrid-Images/assets/58476343/45640723-200d-45b2-93bf-73befc27f692)

## High-Pass Filter
To create a high-pass image for a different but aligned image, we first apply Gaussian blur to it, and then subtract the low-pass filtered version from the original image.

![cat](https://github.com/ibrahimhamada/Hybrid-Images/assets/58476343/2cf60b7e-b0b9-48c4-babc-cc35978f539e)  ![results-high_frequencies](https://github.com/ibrahimhamada/Hybrid-Images/assets/58476343/508788d5-a9d3-4593-bd7e-d570381d134a)

## Hybrid Image
The combination of two pictures can result in a hybrid image, which is illustrated below. To simulate the object's movement closer or farther from your viewpoint, the image is downscaled.


![results-hybrid_image_scales](https://github.com/ibrahimhamada/Hybrid-Images/assets/58476343/26c4c4af-74a3-49e5-9b4f-98b47642c72f)

