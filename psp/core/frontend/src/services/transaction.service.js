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
    const response = await ax.post(`/transactions/${id}/proceed`, {
      payment_method_name: method,
    });

    if (response?.data && response?.data?.payment_url) {
      window.location.href = response.data.payment_url;
    }
  } catch (error) {
    console.error(error);
  }
}
