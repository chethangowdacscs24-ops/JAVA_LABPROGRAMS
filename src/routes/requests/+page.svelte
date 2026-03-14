<script lang="ts">
  import { onMount } from 'svelte';
  import { getHelpRequests } from '$lib/api/client';
  
  let locationFilter = '';
  let helpTypeFilter = '';
  let requests: Array<{
    id: number;
    name: string;
    location: string;
    help_type: string;
    description: string;
    language: string;
    contact_info?: string;
    created_at: string;
  }> = [];
  let loading = false;
  let error = '';
  let totalRequests = 0;

  const helpTypeEmojis: { [key: string]: string } = {
    'housing': '🏠',
    'medical': '🏥',
    'legal': '⚖️',
    'food': '🍽️',
    'other': '❓'
  };

  function getStatusBadge(helpType: string) {
    const statuses: { [key: string]: { badge: string; label: string; icon: string } } = {
      'housing': { badge: 'badge-urgent', label: 'URGENT', icon: '🔴' },
      'medical': { badge: 'badge-urgent', label: 'URGENT', icon: '🔴' },
      'legal': { badge: 'badge-processing', label: 'PROCESSING', icon: '🔵' },
      'food': { badge: 'badge-processing', label: 'PROCESSING', icon: '🔵' },
    };
    return statuses[helpType] || { badge: 'badge-matched', label: 'PENDING', icon: '⚪' };
  }

  function formatTime(dateStr: string) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (hours < 1) return 'just now';
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  }

  async function load() {
    loading = true;
    error = '';
    try {
      const allRequests = await getHelpRequests({
        location: locationFilter || undefined,
        help_type: helpTypeFilter || undefined
      });
      requests = allRequests;
      totalRequests = allRequests.length;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load requests';
      requests = [];
    } finally {
      loading = false;
    }
  }

  onMount(load);

  function handleClearFilters() {
    locationFilter = '';
    helpTypeFilter = '';
  }
</script>

<div class="space-y-8">
  <!-- Header -->
  <div class="space-y-4">
    <div>
      <h1 class="heading-lg text-4xl mb-2">Help Requests</h1>
      <p class="subtext">Browse requests from people in need. Organizations are ready to help.</p>
    </div>
  </div>

  <!-- Filters -->
  <div class="glass-card p-6 space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Location Filter -->
      <div>
        <label for="location" class="text-sm font-semibold text-gray-300 mb-2 block">📍 Location</label>
        <input
          id="location"
          type="text"
          bind:value={locationFilter}
          placeholder="e.g. Berlin, Vienna"
          class="input-base"
        />
      </div>

      <!-- Type Filter -->
      <div>
        <label for="type" class="text-sm font-semibold text-gray-300 mb-2 block">🏷️ Type of Help</label>
        <select bind:value={helpTypeFilter} id="type" class="input-base">
          <option value="">All Types</option>
          <option value="housing">🏠 Housing & Shelter</option>
          <option value="medical">🏥 Medical & Health</option>
          <option value="legal">⚖️ Legal Support</option>
          <option value="food">🍽️ Food & Supplies</option>
          <option value="other">❓ Other</option>
        </select>
      </div>

      <!-- Action Buttons -->
      <div class="sm:col-span-2 lg:col-span-2 flex gap-3 items-end">
        <button on:click={load} disabled={loading} class="btn-primary flex-1">
          {loading ? '🔄 Searching...' : '🔍 Find'}
        </button>
        <button on:click={handleClearFilters} class="btn-secondary flex-1">Clear</button>
      </div>
    </div>
  </div>

  <!-- Error State -->
  {#if error}
    <div class="glass-card bg-red-500/20 border-red-500/50 text-red-300">
      <p>⚠️ {error}</p>
    </div>
  {/if}

  <!-- Loading State -->
  {#if loading}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#each [1, 2, 3, 4] as i}
        <div class="glass-card animate-pulse h-32"></div>
      {/each}
    </div>
  {/if}

  <!-- Empty State -->
  {#if !loading && requests.length === 0 && !error}
    <div class="glass-card bg-gradient-to-r from-blue/5 to-orange/5 border-blue/30 text-center py-12">
      <div class="text-5xl mb-3">🤔</div>
      <h2 class="heading-md mb-2">No requests found</h2>
      <p class="subtext mb-6">
        {locationFilter || helpTypeFilter 
          ? 'Try adjusting your filters or load demo data to see examples.'
          : 'Load demo data to explore the platform.'}
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/" class="btn-secondary">Load Demo Data</a>
        <a href="/submit" class="btn-primary">Submit a Request</a>
      </div>
    </div>
  {/if}

  <!-- Requests List -->
  {#if !loading && requests.length > 0}
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="heading-md flex items-center gap-2">
          📊 {totalRequests} Request{totalRequests !== 1 ? 's' : ''} Found
          <span class="text-xs px-2 py-1 rounded-full bg-blue/20 text-blue font-normal">Live</span>
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#each requests as request, idx (request.id)}
          <a href="/requests/{request.id}" class="glass-card group hover:border-blue/70 hover:bg-white/15 transition-all duration-300 animate-fade-in cursor-pointer" style="animation-delay: {idx * 30}ms">
            <div class="flex items-start justify-between gap-3 mb-3">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1 flex-wrap">
                  <h3 class="font-semibold text-white group-hover:text-blue transition-colors truncate text-lg">
                    {request.name}
                  </h3>
                </div>
                <span class={getStatusBadge(request.help_type).badge}>
                  {getStatusBadge(request.help_type).icon} {getStatusBadge(request.help_type).label}
                </span>
              </div>
              <span class="text-3xl flex-shrink-0">{helpTypeEmojis[request.help_type] || '❓'}</span>
            </div>

            <p class="text-gray-300 text-sm mb-3 line-clamp-2">
              {request.description}
            </p>

            <div class="flex flex-wrap gap-2 text-xs text-gray-400 mb-4">
              <span class="px-2 py-1 bg-white/5 rounded">📍 {request.location}</span>
              <span class="px-2 py-1 bg-white/5 rounded">🗣️ {request.language}</span>
              <span class="px-2 py-1 bg-white/5 rounded">🕐 {formatTime(request.created_at)}</span>
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-white/10">
              <span class="text-xs text-gray-400">Request #{request.id}</span>
              <span class="text-blue group-hover:text-orange transition-colors font-semibold">→ View Details</span>
            </div>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
