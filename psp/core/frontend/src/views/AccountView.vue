<script setup>
import { onBeforeMount, ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import { getMerchantConfig, setMerchantConfig } from '@/services/merchant.service';
import CodeMirror from 'vue-codemirror6';
import { basicSetup } from 'codemirror';
import { yaml } from '@codemirror/lang-yaml';
import { useToast } from "vue-toastification";

const toast = useToast();

const authStore = useAuthStore();

const session = authStore.session;

const apiKeyHidden = ref(true);
const merchantConfig = ref('');
const isLoading = ref(false);

const toggleApiKeyVisibility = () => {
  apiKeyHidden.value = !apiKeyHidden.value;
};

const copyApiKey = () => {
  navigator.clipboard.writeText(session.apiKey || '');
  toast.success('API Key copied to clipboard!');
};

onBeforeMount(async () => {
  await authStore.fetchSession();
  merchantConfig.value = await getMerchantConfig();
});

const saveConfig = async () => {
  isLoading.value = true;
  try {
    console.log(merchantConfig.value.yaml)
    await setMerchantConfig({
      yaml: merchantConfig.value.yaml,
    });
    toast.success('Configuration saved successfully');
  } catch (error) {
    toast.error('Failed to save configuration');
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="flex flex-col w-full items-center min-h-screen bg-zinc-800 text-zinc-300 p-6">
    <div class="w-2/3 p-6 bg-zinc-700 rounded-md shadow-md mt-20">
      <h2 class="text-lg font-semibold mb-4">Account Information</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Username</label>
          <p class="mt-1 text-zinc-400">{{ session.username }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium">Title</label>
          <p class="mt-1 text-zinc-400">{{ session.title }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium">API Key</label>
          <div class="mt-1 flex items-center">
            <input
              type="text"
              :value="apiKeyHidden ? 'psp_••••••••••••••••••••••••••••••••••••••••••' : session.apiKey"
              readonly
              class="flex-1 rounded-md bg-zinc-900 text-zinc-400 px-3 py-1"
            />
            <button
              @click="toggleApiKeyVisibility"
              class="ml-2 px-3 py-1 rounded-md bg-red-400 text-zinc-800 hover:bg-red-500"
            >
              {{ apiKeyHidden ? 'Show' : 'Hide' }}
            </button>
            <button
              @click="copyApiKey"
              class="ml-2 px-3 py-1 rounded-md bg-red-400 text-zinc-800 hover:bg-red-500"
            >
              Copy
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Merchant Configuration -->
    <div class="w-2/3 mt-8 p-6 bg-zinc-700 rounded-md shadow-md">
      <h2 class="text-lg w-full font-semibold mb-4">Merchant Configuration</h2>
      <code-mirror
        v-model="merchantConfig.yaml"
        :extensions="[basicSetup, yaml()]"
        class="h-full bg-sky-600 rounded-md"
      />
      <div class="mt-4 flex justify-end space-x-2">
        <button
          @click="saveConfig"
          class="px-4 py-2 rounded-md bg-red-400 text-zinc-800 hover:bg-red-500"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>
