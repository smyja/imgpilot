import { blobToBase64 } from "@/lib/utils";

export const fetchImage = async (
  input_image: string,
  prompt: string,
  api_key: string,
  signal?: AbortSignal
) => {
  const base64Data = input_image.replace(/^data:image\/(png|jpeg);base64,/, "");
  const binaryData = atob(base64Data);
  const arrayBuffer = new ArrayBuffer(binaryData.length);
  const uint8Array = new Uint8Array(arrayBuffer);

  for (let i = 0; i < binaryData.length; i++) {
    uint8Array[i] = binaryData.charCodeAt(i);
  }

  const blob = new Blob([arrayBuffer], { type: "image/jpeg" }); // Adjust the mime type accordingly

  const formData = new FormData();
  formData.append("init_image", blob);
  formData.append("image_strength", "0.35");
  formData.append("init_image_mode", "IMAGE_STRENGTH");
  formData.append("text_prompts[0][text]", prompt);
  formData.append("text_prompts[0][weight]", "1");
  formData.append("cfg_scale", "7");
  formData.append("clip_guidance_preset", "FAST_BLUE");
  formData.append("sampler", "K_DPM_2_ANCESTRAL");
  formData.append("samples", "3");
  formData.append("steps", "30");

  const response = await fetch(
    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image",
    {
      headers: {
        Authorization: `Bearer sk-DxMTg0eRrS8oBrbHnvnkoB5rHll97NRJjpJasZpYXsRyzrl9`,
      },
      body: formData,
      method: "POST",
      signal,
    },
  );

  if (response.status !== 200) {
    throw new Error("Failed to fetch image");
  }

  const resultBlob = await response.blob();
  return await blobToBase64(resultBlob);
};
