import { ax } from "@/utils/axios";

export const pay = async (id, data) => {
  try {
    const response = await ax.post(`/transactions/${id}/pay`, data);

    const data = response.data;
    
    window.location.href = data.next_url;

    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}
