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

export const proceedWithTransaction = async (id, method) => {
  try {
    await ax.post(`/transactions/${id}/proceed`, {
      payment_method_name: method,
    });
  } catch (error) {
    console.error(error);
  }
}
