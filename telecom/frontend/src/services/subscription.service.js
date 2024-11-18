import { ax } from '@/utils/axios';

// export async function getServices(successCallback, errorCallback) {
//   ax({ requiresAuth: true }).get('/api/services')
//   .then(res => {
//     if (res.data) successCallback(res.data)
//     else errorCallback()
//   })
//   .catch(err => {
//     console.log(err)
//     errorCallback()
//   })
// }

// export async function placeOrder(services, successCallback, errorCallback) {
//   ax({ requiresAuth: true }).post('/api/account/subscriptions', { services }, {
//     validateStatus: (status) => {
//       if (status === 302) return true;
//       return false;
//     }
//   })
//   .then(res => {
//     if (res.data.location) successCallback(res.data.location)
//     else errorCallback()
//   })
//   .catch(err => {
//     console.log(err)
//     errorCallback()
//   })
// }
