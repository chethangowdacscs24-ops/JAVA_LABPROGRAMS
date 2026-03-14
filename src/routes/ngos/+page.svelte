<script lang="ts">
  import { getNgosNearby } from '$lib/api/client';
  
  let locationFilter = '';
  let ngos: Array<{ id: number; name: string; services: string; location: string; contact_info: string }> = [];
  let loading = false;
  let error = '';
  let searched = false;

  const serviceIcons: { [key: string]: string } = {
    'housing': '🏠',
    'medical': '🏥',
    'legal': '⚖️',
    'food': '🍽️',
    'education': '🎓',
    'mental health': '🧠',
    'refugee': '🛡️',
    'clothing': '👕',
    'transportation': '🚌',
  };

  function getServiceIcon(service: string): string {
    const lower = service.toLowerCase();
    for (const key in serviceIcons) {
      if (lower.includes(key)) {
        return serviceIcons[key];
      }
    }
    return '🏢';
  }

  async function load() {
    if (!locationFilter.trim()) {
      error = 'Please enter a location to search for NGOs.';
      ngos = [];
      searched = false;
      return;
    }
    loading = true;
    error = '';
    searched = true;
    try {
      ngos = await getNgosNearby(locationFilter);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load NGOs';
      ngos = [];
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      load();
    }
  }
</script>

<div class="space-y-8">
  <!-- Header -->
  <div class="space-y-4">
    <div>
      <h1 class="heading-lg text-4xl mb-2">Find Organizations</h1>
      <p class="subtext">Discover verified NGOs and organizations ready to help in your area.</p>
    </div>
  </div>

  <!-- Search Card -->
  <div class="glass-card p-6 sm:p-8 space-y-4">
    <div class="space-y-3">
      <label for="location" class="text-sm font-semibold text-gray-300">🌍 Search by City or Location</label>
      <div class="flex flex-col sm:flex-row gap-3">
        <input
          id="location"
          type="text"
          bind:value={locationFilter}
          on:keydown={handleKeydown}
          placeholder="e.g. Berlin, Vienna, Prague"
          class="input-base flex-1"
        />
        <button on:click={load} disabled={loading} class="btn-primary whitespace-nowrap">
          {loading ? '🔄 Searching...' : '🔍 Search'}
        </button>
      </div>
    </div>
    <p class="text-xs text-gray-400">
      💡 Enter a city name to find active organizations in that area. Organizations match help requests automatically.
    </p>
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
        <div class="glass-card animate-pulse h-40"></div>
      {/each}
    </div>
  {/if}

  <!-- Empty State -->
  {#if !loading && ngos.length === 0 && searched}
    <div class="glass-card bg-gradient-to-r from-orange/5 to-red-500/5 border-orange/30 text-center py-12">
      <div class="text-5xl mb-3">🔍</div>
      <h2 class="heading-md mb-2">No organizations found</h2>
      <p class="subtext mb-6">
        No registered NGOs yet for "{locationFilter}". Be the first to register your organization!
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/ngos/register" class="btn-accent">Register Organization</a>
        <a href="/" class="btn-secondary">Load Demo Data</a>
      </div>
    </div>
  {/if}

  <!-- Initial State -->
  {#if !searched && !loading && ngos.length === 0}
    <div class="glass-card bg-gradient-to-r from-blue/5 to-blue-dark/5 border-blue/30 text-center py-12">
      <div class="text-5xl mb-3">👥</div>
      <h2 class="heading-md mb-2">Ready to Find Help?</h2>
      <p class="subtext mb-6">
        Search for organizations in your area that can provide support with housing, medical care, legal services, and more.
      </p>
      <a href="/ngos/register" class="btn-primary">Register Your Organization</a>
    </div>
  {/if}

  <!-- NGOs Grid -->
  {#if !loading && ngos.length > 0}
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="heading-md flex items-center gap-2">
          🏢 {ngos.length} Organization{ngos.length !== 1 ? 's' : ''} Found
          <span class="text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-300 font-normal">Active</span>
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#each ngos as org, idx (org.id)}
          <div class="glass-card group hover:border-orange/70 hover:bg-white/15 transition-all duration-300 animate-fade-in space-y-4" style="animation-delay: {idx * 30}ms">
            <!-- Organization Header -->
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-white group-hover:text-orange transition-colors truncate text-lg mb-1">
                  {org.name}
                </h3>
                <p class="text-xs text-gray-400">📍 {org.location}</p>
              </div>
              <span class="text-3xl flex-shrink-0">🏢</span>
            </div>

            <!-- Services -->
            <div>
              <p class="text-xs text-gray-400 mb-2">Services:</p>
              <div class="flex flex-wrap gap-2">
                {#each org.services.split(',').map(s => s.trim()).slice(0, 3) as service}
                  <span class="px-2 py-1 bg-white/10 border border-white/20 rounded text-xs text-gray-300">
                    {getServiceIcon(service)} {service}
                  </span>
                {/each}
                {#if org.services.split(',').length > 3}
                  <span class="px-2 py-1 bg-blue/20 border border-blue/50 rounded text-xs text-blue">
                    +{org.services.split(',').length - 3} more
                  </span>
                {/if}
              </div>
            </div>

            <!-- Contact Section -->
            <div class="pt-4 border-t border-white/10">
              <p class="text-xs text-gray-400 mb-2">Contact:</p>
              <p class="text-sm font-mono break-all text-blue group-hover:text-orange transition-colors">
                {org.contact_info}
              </p>
            </div>

            <!-- Action -->
            <div class="flex gap-2">
              <button class="btn-secondary flex-1 text-sm">📋 View Details</button>
              <button class="btn-primary text-sm px-3">📞</button>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Register CTA -->
  <div class="glass-card bg-gradient-to-r from-blue/10 to-blue-dark/10 border-blue/50 text-center py-8 sm:py-12 space-y-4">
    <h2 class="heading-md">Join the Network</h2>
    <p class="subtext max-w-lg mx-auto">
      Is your organization ready to help? Register with ASYLUM to get connected with people in need and match them with your services.
    </p>
    <a href="/ngos/register" class="btn-primary inline-block">🚀 Register Your Organization</a>
  </div>
</div>
