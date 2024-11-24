<script setup>
  import { ref } from 'vue';

  const cardHolder = ref('');
  const cardNumber = ref('');
  const expiryDate = ref('');
  const cvv = ref('');
  const cardHolderErrorMessage = ref('');
  const cardNumberErrorMessage = ref('');
  const expiryDateErrorMessage = ref('');
  const cvvErrorMessage = ref('');

  const resetErrorMessages = () => {
    cardHolderErrorMessage.value = '';
    cardNumberErrorMessage.value = '';
    expiryDateErrorMessage.value = '';
    cvvErrorMessage.value = '';
  };

  const handlePay = () => {
    if (isDataValid()) {
      // proceed
    }
  };

  const isDataValid = () => {
    let valid = true;
    if (cardHolder.value.trim().length === 0) {
      cardHolderErrorMessage.value = 'Card holder name cannot be empty';
      valid = false;
    }
    if (cardNumber.value.trim().length === 0) {
      cardNumberErrorMessage.value = 'Card number cannot be empty';
      valid = false;
    }
    else if (!cardNumber.value.replace(/\s/g, '').match(/^[\d]{16}$/g)) {
      cardNumberErrorMessage.value = 'Card number invalid';
      valid = false;
    }
    if (expiryDate.value.trim().length === 0) {
      expiryDateErrorMessage.value = 'Expiry date cannot be empty';
      valid = false;
    }
    else if (!expiryDate.value.match(/^[\d]{2}\/[\d]{2}$/g)) {
      expiryDateErrorMessage.value = 'Expiry date invalid';
      valid = false;
    }
    else if (Number(expiryDate.value.slice(0,2)) > 12 || Number(expiryDate.value.slice(0,2)) < 1) {
      expiryDateErrorMessage.value = 'Expiry date invalid';
      valid = false;
    }
    else if (Number(expiryDate.value.slice(0,2)) > 12 || Number(expiryDate.value.slice(0,2)) < 1) {
      expiryDateErrorMessage.value = 'Expiry date invalid';
      valid = false;
    }
    if (cvv.value.trim().length === 0) {
      cvvErrorMessage.value = 'CVV cannot be empty';
      valid = false;
    }
    else if (!cvv.value.match(/^[\d]{3}$/g)) {
      cvvErrorMessage.value = 'CVV invalid';
      valid = false;
    }
    return valid
  };

  const formatCardNumber = () => {
    if (cardNumber.value.replace(/\s/g, '').length > 16) {
      cardNumber.value = cardNumber.value.replace(/\s/g, '').slice(0, 16);
    }
    var strippedInput = cardNumber.value.replace(/\s/g, '');
    var formattedInput = strippedInput.replace(/(\d{4})(?=\d)/g, '$1 ');
    cardNumber.value = formattedInput;
  };

  const formatExpiryDate = () => {
    if (expiryDate.value.replace(/\s/g, '').replace('/', '').length > 4) {
      expiryDate.value = expiryDate.value.replace(/\s/g, '').replace('/', '').slice(0, 4);
    }
    var strippedInput = expiryDate.value.replace(/\s/g, '');
    var formattedInput = strippedInput.replace(/(\d{2})(?=\d)/g, '$1/');
    expiryDate.value = formattedInput;
  };

  const formatCvv = () => {
    if (cvv.value.replace(/\s/g, '').length > 3) {
      cvv.value = cvv.value.replace(/\s/g, '').replace('/', '').slice(0, 3);
    }
  };

</script>

<template>
  <div class="relative flex flex-col justify-center min-h-screen bg-gray-50">
    <div class="flex flex-col justify-between mx-4 md:mx-auto md:w-108 h-96 p-4">
      <div class="flex flex-col">
        <div class="text-sm text-center tracking-wide">Please fill in your card details to proceed with the payment</div>
        <div class="flex flex-col gap-y-4 mt-8">
          <div class="w-full">
            <label class="block tracking-wide text-xs font-bold mb-1"
            for="card-number-input">
              Card Number*
            </label>
            <input class="appearance-none block w-full tracking-wide bg-white shadow-inner
            placeholder-medium caret-medium border px-2 py-2 rounded-lg leading-tight outline-none
            focus:transition-color duration-300" @input="formatCardNumber(); resetErrorMessages();"
            id="card-number-input" type="text" placeholder="0000 0000 0000 0000" autofocus="autofocus"
            :class="[ cardNumberErrorMessage ? 'border-red-500' : 'border-stone-300 focus:border-accent' ]"
            v-model="cardNumber">
            <div class="h-1">
              <p v-if="cardNumberErrorMessage.length !== 0" class="text-red-500 text-xs">
                {{ cardNumberErrorMessage }}
              </p>
            </div>
          </div>

          <div class="w-full">
            <label class="block tracking-wide text-xs font-bold mb-1"
            for="card-holder-input">
              Card Holder*
            </label>
            <input class="appearance-none block w-full tracking-wide bg-white shadow-inner
            placeholder-medium caret-medium border px-2 py-2 rounded-lg leading-tight outline-none
            focus:transition-color duration-300" @input="resetErrorMessages()"
            id="card-holder-input" type="text" placeholder="Name on the card" autofocus="autofocus"
            :class="[ cardHolderErrorMessage ? 'border-red-500' : 'border-stone-300 focus:border-accent' ]"
            v-model="cardHolder">
            <div class="h-1">
              <p v-if="cardHolderErrorMessage.length !== 0" class="text-red-500 text-xs">
                {{ cardHolderErrorMessage }}
              </p>
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-x-6">
            <div class="w-full">
              <label class="block tracking-wide text-xs font-bold mb-1"
              for="expiry-date-input">
                Expiry Date*
              </label>
              <input class="appearance-none block w-full tracking-wide bg-white shadow-inner
              placeholder-medium caret-medium border px-2 py-2 rounded-lg leading-tight outline-none
              focus:transition-color duration-300" @input="formatExpiryDate(); resetErrorMessages();"
              id="expiry-date-input" type="text" placeholder="MM/YY" autofocus="autofocus"
              :class="[ expiryDateErrorMessage ? 'border-red-500' : 'border-stone-300 focus:border-accent' ]"
              v-model="expiryDate">
              <div class="h-1">
                <p v-if="expiryDateErrorMessage.length !== 0" class="text-red-500 text-xs">
                  {{ expiryDateErrorMessage }}
                </p>
              </div>
            </div>
            
            <div class="w-full">
              <label class="block tracking-wide text-xs font-bold mb-1"
              for="cvv-input" title="The three digit number on the back of your card">
                CVV*
              </label>
              <input class="appearance-none block w-full tracking-wide bg-white shadow-inner
              placeholder-medium caret-medium border px-2 py-2 rounded-lg leading-tight outline-none
              focus:transition-color duration-300" @input="formatCvv(); resetErrorMessages();"
              id="cvv-input" type="text" placeholder="---" autofocus="autofocus"
              :class="[ cvvErrorMessage ? 'border-red-500' : 'border-stone-300 focus:border-accent' ]"
              v-model="cvv">
              <div class="h-1">
                <p v-if="cvvErrorMessage.length !== 0" class="text-red-500 text-xs">
                  {{ cvvErrorMessage }}
                </p>
              </div>
            </div>


          </div>

        </div>
      </div>

      <button class="bg-white border-2 border-accent py-2 rounded-lg text-zinc-700
      font-medium hover:bg-accent hover:bg-opacity-30 shadow-sm"
      @click="handlePay">
        Pay
      </button>

    </div>
  </div>
</template>
