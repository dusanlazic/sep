<template>
  <nav class="absolute top-0 right-left w-full bg-white shadow z-10">
    <div class="container mx-auto px-6 py-3 flex items-center justify-between">
      <RouterLink to="/" class="font-medium text-xl text-violet-500">
        Telecom Serbia
      </RouterLink>
      <div>
        <RouterLink
          to="/login"
        >
          <button class="px-4 py-1 text-black font-medium border border-black border-dashed rounded hover:bg-violet-300 text-sm">Log In</button>
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
