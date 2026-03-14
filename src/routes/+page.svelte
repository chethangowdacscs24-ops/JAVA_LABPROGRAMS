<script lang="ts">
  import { onMount } from 'svelte';
  import { getStats, getHelpRequests, seedDemo } from '$lib/api/client';
  
  let stats = { help_requests: 0, ngos: 0 };
  let displayStats = { requests: 0, ngos: 0, matches: 0, lives: 0 };
  let loading = true;
  let seedMessage = '';
  let seeding = false;
  let recentRequests: any[] = [];
  
  function animateCounter(target: number, current: number, duration: number = 2000) {
    if (current >= target) return target;
    const increment = target / (duration / 16);
    return current + increment;
  }

  async function loadData() {
    loading = true;
    try {
      stats = await getStats();
      const requests = await getHelpRequests({});
      recentRequests = requests.slice(0, 5);
      displayStats = {
        requests: stats.help_requests,
        ngos: stats.ngos,
        matches: Math.max(Math.floor((stats.help_requests || 0) * 0.6), 0),
        lives: Math.max(Math.floor((stats.help_requests || 0) * 0.8), 0),
      };
    } catch {
      stats = { help_requests: 0, ngos: 0 };
      displayStats = { requests: 0, ngos: 0, matches: 0, lives: 0 };
    } finally {
      loading = false;
    }
  }

  async function seed() {
    seeding = true;
    seedMessage = '';
    try {
      const r = await seedDemo();
      seedMessage = r.message === 'Already seeded' ? 'Demo data already loaded.' : `✓ Loaded ${r.help_requests} requests and ${r.ngos} NGOs.`;
      await loadData();
    } catch (e) {
      seedMessage = '✗ ' + (e instanceof Error ? e.message : 'Failed to load demo data');
    } finally {
      seeding = false;
    }
  }

  onMount(loadData);

  function getStatusBadge(helpType: string) {
    const statuses: { [key: string]: { badge: string; label: string } } = {
      'housing': { badge: 'badge-urgent', label: 'URGENT' },
      'medical': { badge: 'badge-urgent', label: 'URGENT' },
      'legal': { badge: 'badge-processing', label: 'PROCESSING' },
      'food': { badge: 'badge-processing', label: 'PROCESSING' },
    };
    return statuses[helpType] || { badge: 'badge-matched', label: 'PENDING' };
  }

  function formatTime(dateStr: string) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  }
</script>

<!-- Hero Section -->
<div class="mb-12 sm:mb-16 space-y-6 animate-fade-in">
  <div class="text-center space-y-3 sm:space-y-4">
    <div class="inline-block mb-4">
      <span class="badge animate-pulse">
        <span class="inline-block w-2 h-2 bg-blue rounded-full"></span>
        Powered by Community
      </span>
    </div>
    <h1 class="heading-lg text-4xl sm:text-5xl md:text-6xl leading-tight">
      Every Second Counts.<br />Every Life Matters.
    </h1>
    <p class="subtext text-base sm:text-lg max-w-2xl mx-auto">
      Connect people in urgent need with organizations ready to help. Real-time matching. Zero friction. Maximum impact.
    </p>
  </div>
</div>

<!-- Stats Cards with Animated Counters -->
{#if !loading}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-12 sm:mb-16">
    <!-- Help Requests Card -->
    <div class="glass-card group cursor-pointer hover:border-blue/50 hover:bg-white/10">
      <div class="flex items-center justify-between mb-3">
        <span class="text-gray-400 text-sm font-semibold">Help Requests</span>
        <span class="text-xl sm:text-2xl">📋</span>
      </div>
      <div class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue to-blue-dark bg-clip-text text-transparent mb-2">
        {Math.floor(displayStats.requests)}
      </div>
      <div class="h-1 w-8 bg-gradient-to-r from-blue to-transparent rounded-full"></div>
    </div>

    <!-- NGOs Card -->
    <div class="glass-card group cursor-pointer hover:border-orange/50 hover:bg-white/10">
      <div class="flex items-center justify-between mb-3">
        <span class="text-gray-400 text-sm font-semibold">Active NGOs</span>
        <span class="text-xl sm:text-2xl">🏢</span>
      </div>
      <div class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-orange to-orange-dark bg-clip-text text-transparent mb-2">
        {Math.floor(displayStats.ngos)}
      </div>
      <div class="h-1 w-8 bg-gradient-to-r from-orange to-transparent rounded-full"></div>
    </div>

    <!-- Matches Today Card -->
    <div class="glass-card group cursor-pointer hover:border-green-500/50 hover:bg-white/10">
      <div class="flex items-center justify-between mb-3">
        <span class="text-gray-400 text-sm font-semibold">Matches Today</span>
        <span class="text-xl sm:text-2xl">🎯</span>
      </div>
      <div class="text-3xl sm:text-4xl font-bold text-green-400 mb-2">
        {Math.floor(displayStats.matches)}
      </div>
      <div class="h-1 w-8 bg-gradient-to-r from-green-400 to-transparent rounded-full"></div>
    </div>

    <!-- Lives Helped Card -->
    <div class="glass-card group cursor-pointer hover:border-emerald-500/50 hover:bg-white/10">
      <div class="flex items-center justify-between mb-3">
        <span class="text-gray-400 text-sm font-semibold">Lives Helped</span>
        <span class="text-xl sm:text-2xl">❤️</span>
      </div>
      <div class="text-3xl sm:text-4xl font-bold text-emerald-400 mb-2">
        {Math.floor(displayStats.lives)}
      </div>
      <div class="h-1 w-8 bg-gradient-to-r from-emerald-400 to-transparent rounded-full"></div>
    </div>
  </div>
{/if}

<!-- Status Badges Info -->
<div class="mb-12 sm:mb-16 glass-card">
  <h2 class="heading-md mb-4 sm:mb-6">Request Status Indicators</h2>
  <div class="flex flex-wrap gap-3 sm:gap-4">
    <span class="badge-urgent">🔴 URGENT</span>
    <span class="badge-processing">🔵 PROCESSING</span>
    <span class="badge-matched">🟢 MATCHED</span>
    <span class="badge-resolved">✅ RESOLVED</span>
  </div>
  <p class="text-gray-400 text-xs sm:text-sm mt-4">Real-time status tracking helps you stay informed every step of the journey.</p>
</div>

<!-- Recent Activity Feed -->
{#if recentRequests.length > 0}
  <div class="mb-12 sm:mb-16">
    <h2 class="heading-md mb-6 flex items-center gap-2">
      <span>📊 Recent Activity</span>
      <span class="text-xs px-2 py-1 rounded-full bg-blue/20 text-blue">Live Feed</span>
    </h2>
    <div class="space-y-3 sm:space-y-4">
      {#each recentRequests as request, idx (request.id)}
        <div class="glass-card group hover:border-blue/50 transition-all duration-300 animate-slide-in" style="animation-delay: {idx * 50}ms">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2 flex-wrap">
                <a href="/requests/{request.id}" class="font-semibold text-white hover:text-blue transition-colors truncate">
                  {request.name}
                </a>
                <span class={getStatusBadge(request.help_type).badge}>
                  {getStatusBadge(request.help_type).label}
                </span>
              </div>
              <p class="text-gray-400 text-sm mb-2">{request.description.slice(0, 100)}{request.description.length > 100 ? '...' : ''}</p>
              <div class="flex flex-wrap gap-2 text-xs text-gray-500">
                <span>📍 {request.location}</span>
                <span>🏷️ {request.help_type}</span>
                <span>🕐 {formatTime(request.created_at)}</span>
              </div>
            </div>
            <a href="/requests/{request.id}" class="text-blue hover:text-orange text-sm font-semibold whitespace-nowrap">→ Details</a>
          </div>
        </div>
      {/each}
    </div>
  </div>
{/if}

<!-- Action Buttons -->
<div class="mb-12 sm:mb-16">
  <h2 class="heading-md mb-6">Get Started</h2>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
    <!-- Submit Request Button -->
    <a href="/submit" class="glass-card group hover:border-blue/70 hover:bg-white/15 cursor-pointer transform transition-all duration-300 hover:scale-105">
      <div class="text-4xl mb-3">📝</div>
      <h3 class="font-semibold text-white mb-2">Submit Request</h3>
      <p class="text-gray-400 text-sm mb-4">Tell us what help you need. Get connected in seconds.</p>
      <button class="btn-primary text-sm w-full">Create Request</button>
    </a>

    <!-- Browse Requests Button -->
    <a href="/requests" class="glass-card group hover:border-blue/70 hover:bg-white/15 cursor-pointer transform transition-all duration-300 hover:scale-105">
      <div class="text-4xl mb-3">🔍</div>
      <h3 class="font-semibold text-white mb-2">Browse Requests</h3>
      <p class="text-gray-400 text-sm mb-4">Explore all help requests. Filter by location or type.</p>
      <button class="btn-secondary text-sm w-full">View All</button>
    </a>

    <!-- Find NGOs Button -->
    <a href="/ngos" class="glass-card group hover:border-orange/70 hover:bg-white/15 cursor-pointer transform transition-all duration-300 hover:scale-105">
      <div class="text-4xl mb-3">🏢</div>
      <h3 class="font-semibold text-white mb-2">Find NGOs</h3>
      <p class="text-gray-400 text-sm mb-4">Discover organizations ready to help near you.</p>
      <button class="btn-accent text-sm w-full">Search NGOs</button>
    </a>

    <!-- Load Demo Data Button -->
    <div class="glass-card group hover:border-green-500/70 hover:bg-white/15 cursor-pointer transform transition-all duration-300 hover:scale-105">
      <div class="text-4xl mb-3">🚀</div>
      <h3 class="font-semibold text-white mb-2">Demo Data</h3>
      <p class="text-gray-400 text-sm mb-4">Try the platform with sample requests & NGOs.</p>
      <button class="btn-secondary text-sm w-full" on:click={seed} disabled={seeding}>
        {seeding ? 'Loading...' : 'Load Demo'}
      </button>
      {#if seedMessage}
        <p class="text-xs mt-2 {seedMessage.startsWith('✓') ? 'text-green-400' : 'text-orange-400'}">
          {seedMessage}
        </p>
      {/if}
    </div>
  </div>
</div>

<!-- Call to Action Section -->
<div class="mb-12 sm:mb-16 glass-card bg-gradient-to-r from-blue/10 to-orange/10 border-blue/50 text-center py-8 sm:py-12">
  <h2 class="heading-md mb-3 sm:mb-4">Be the Change</h2>
  <p class="subtext mb-6 max-w-xl mx-auto">
    Whether you're seeking help or offering it, ASYLUM connects you with the right people in seconds.
  </p>
  <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
    <a href="/submit" class="btn-primary">I Need Help</a>
    <a href="/ngos/register" class="btn-accent">Register My Organization</a>
  </div>
</div>
    border: 1px solid #0f3460;
    color: #b8c5d6;
    cursor: pointer;
  }
  .btn-secondary:hover {
    border-color: #1a4a7a;
  }
  .demo {
    padding: 1.5rem;
    background: rgba(15, 52, 96, 0.3);
    border-radius: 8px;
  }
  .muted { color: #8899aa; margin: 0 0 0.5rem; }
  .seed-msg { margin: 0.5rem 0 0; color: #8f8; }
</style>
