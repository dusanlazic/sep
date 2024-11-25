import { ax } from "@/utils/axios";

export const getMerchantConfig = async () => {
  try {
    const response = await ax.get(`/payment-methods/config`);
    
    if (!response?.data) {
      return null;
    }

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export const setMerchantConfig = async (data) => {
  try {
    const response = await ax.post(`/payment-methods/config`, data);
    
    if (!response?.data) {
      return null;
    }

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};
