import { ax } from "@/utils/axios";

export const getTransaction = async (id) => {
  try {
    const response = await ax.get(`/transactions/${id}`);
    
    if (!response?.data) {
      return null;
    }

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};
