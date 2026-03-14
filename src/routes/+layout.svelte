<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { getStats } from '$lib/api/client';

  let stats = { help_requests: 0, ngos: 0 };
  let pending = 3;
  let ngoOnline = 2;

  onMount(async () => {
    try {
      stats = await getStats();
    } catch {
      stats = { help_requests: 0, ngos: 0 };
    }
  });
</script>

<!-- Ticker Bar -->
<div class="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-navy via-navy to-navy-light border-b border-white/10 backdrop-blur-md">
  <div class="px-4 py-2 flex items-center gap-3 text-sm sm:text-base font-medium text-gray-300">
    <div class="flex items-center gap-2 animate-pulse">
      <span class="inline-block w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
      <span>LIVE</span>
    </div>
    <span class="hidden sm:inline">•</span>
    <span class="hidden sm:inline">🎯 {pending} pending requests</span>
    <span class="hidden sm:inline">•</span>
    <span class="hidden sm:inline">👥 {ngoOnline} NGOs online</span>
    <span class="inline sm:hidden">→ {pending} pending | {ngoOnline} NGOs</span>
  </div>
</div>

<!-- Navigation -->
<nav class="fixed top-12 sm:top-10 left-0 right-0 z-40 bg-gradient-to-b from-navy via-navy to-transparent backdrop-blur-md border-b border-white/5">
  <div class="max-w-7xl mx-auto px-4 py-3 sm:py-4 flex items-center justify-between gap-4 sm:gap-8">
    <a href="/" class="text-xl sm:text-2xl font-black bg-gradient-to-r from-blue to-orange bg-clip-text text-transparent hover:from-orange hover:to-blue transition-all duration-300 no-underline">
      ASYLUM
    </a>
    
    <div class="flex items-center gap-2 sm:gap-6 text-sm sm:text-base overflow-x-auto">
      <a href="/" class="whitespace-nowrap px-3 py-1 rounded-lg text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200 no-underline">Home</a>
      <a href="/submit" class="whitespace-nowrap px-3 py-1 rounded-lg text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200 no-underline">Request</a>
      <a href="/requests" class="whitespace-nowrap px-3 py-1 rounded-lg text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200 no-underline">Browse</a>
      <a href="/ngos" class="whitespace-nowrap px-3 py-1 rounded-lg text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200 no-underline">NGOs</a>
      <a href="/ngos/register" class="whitespace-nowrap px-3 py-1 rounded-lg text-blue hover:text-orange transition-all duration-200 font-semibold no-underline">Register</a>
    </div>
  </div>
</nav>

<!-- Main Content -->
<main class="min-h-screen bg-navy pt-32 sm:pt-28 pb-20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <slot />
  </div>
</main>

<!-- Footer -->
<footer class="bg-gradient-to-t from-navy-light via-navy to-transparent border-t border-white/10 backdrop-blur-md px-4 sm:px-6 py-8 sm:py-12 text-center text-gray-400 text-xs sm:text-sm">
  <p class="mb-2 font-semibold text-gray-300">ASYLUM — Every Second Counts. Every Life Matters.</p>
  <p>Connect people in need with organizations that can help. No login required.</p>
  <p class="text-gray-500 mt-4 text-xs">© 2026 ASYLUM. Built for impact.</p>
</footer>
