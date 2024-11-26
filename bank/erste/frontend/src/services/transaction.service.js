import { ax } from "@/utils/axios";

export const pay = async (id, data) => {
  try {
    const response = await ax.post(`/transactions/${id}/pay`, data);

    const responseData = response.data;
    
    if (responseData && responseData.next_url) {
      window.location.href = responseData.next_url;
    }

    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}
