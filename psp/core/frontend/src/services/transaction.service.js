
export const getTransaction = async (id) => {
  try {
    const response = await ax.post(`/transactions/${id}`);

    console.log(response.data);
    
    if (!response?.data) {
      return false;
    }

    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
};
