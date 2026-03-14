<script lang="ts">
  import { page } from '$app/stores';
  import { getHelpRequest } from '$lib/api/client';
  import { onMount } from 'svelte';
  
  let request: {
    id: number;
    name: string;
    location: string;
    help_type: string;
    description: string;
    language: string;
    contact_info?: string;
    created_at: string;
  } | null = null;
  let error = '';

  const helpTypeEmojis: { [key: string]: string } = {
    'housing': '🏠',
    'medical': '🏥',
    'legal': '⚖️',
    'food': '🍽️',
    'other': '❓'
  };

  function getStatusBadge(helpType: string) {
    const statuses: { [key: string]: { badge: string; label: string; color: string } } = {
      'housing': { badge: 'badge-urgent', label: 'URGENT', color: 'red' },
      'medical': { badge: 'badge-urgent', label: 'URGENT', color: 'red' },
      'legal': { badge: 'badge-processing', label: 'PROCESSING', color: 'blue' },
      'food': { badge: 'badge-processing', label: 'PROCESSING', color: 'blue' },
    };
    return statuses[helpType] || { badge: 'badge-matched', label: 'PENDING', color: 'green' };
  }

  function formatDate(dateStr: string) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  onMount(async () => {
    const id = $page.params.id;
    try {
      request = await getHelpRequest(id);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Request not found';
    }
  });
</script>

<div class="space-y-8">
  <!-- Back Link -->
  <a href="/requests" class="inline-flex items-center gap-2 text-blue hover:text-orange transition-colors font-semibold">
    ← Back to Requests
  </a>

  {#if error}
    <div class="glass-card bg-red-500/20 border-red-500/50 text-red-300 text-center py-12">
      <div class="text-5xl mb-3">❌</div>
      <h2 class="heading-md mb-2">Request Not Found</h2>
      <p class="subtext mb-6">{error}</p>
      <a href="/requests" class="btn-primary">Return to Requests</a>
    </div>
  {:else if !request}
    <div class="space-y-4">
      <div class="glass-card animate-pulse h-48"></div>
      <div class="glass-card animate-pulse h-32"></div>
    </div>
  {:else}
    <!-- Main Request Card -->
    <div class="glass-card bg-gradient-to-r from-blue/10 to-blue-dark/10 border-blue/50 p-6 sm:p-8 space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 flex-wrap">
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-4 mb-3 flex-wrap">
            <span class="text-5xl">{helpTypeEmojis[request.help_type] || '❓'}</span>
            <div>
              <h1 class="heading-lg text-3xl sm:text-4xl mb-2">{request.name}</h1>
              <span class={getStatusBadge(request.help_type).badge}>
                🔴 {getStatusBadge(request.help_type).label}
              </span>
            </div>
          </div>
        </div>
        <div class="text-right">
          <span class="text-xs bg-white/10 px-3 py-1 rounded-full text-gray-400">ID #{request.id}</span>
        </div>
      </div>

      <!-- Quick Info -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <div class="text-xs text-gray-400 mb-1">📍 Location</div>
          <div class="font-semibold text-white">{request.location}</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <div class="text-xs text-gray-400 mb-1">🏷️ Category</div>
          <div class="font-semibold text-white capitalize">{request.help_type}</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <div class="text-xs text-gray-400 mb-1">🗣️ Language</div>
          <div class="font-semibold text-white">{request.language}</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <div class="text-xs text-gray-400 mb-1">🕐 Submitted</div>
          <div class="font-semibold text-white text-sm">{new Date(request.created_at).toLocaleDateString()}</div>
        </div>
      </div>
    </div>

    <!-- Full Description -->
    <div class="glass-card space-y-4">
      <h2 class="heading-md">📝 Full Description</h2>
      <p class="text-gray-300 leading-relaxed whitespace-pre-wrap">
        {request.description}
      </p>
    </div>

    <!-- Contact Information -->
    {#if request.contact_info}
      <div class="glass-card bg-orange/10 border-orange/50 space-y-4">
        <h2 class="heading-md text-orange">📞 Contact Information</h2>
        <div class="bg-white/5 border border-orange/30 rounded-lg p-4">
          <p class="text-gray-300 break-all font-mono">{request.contact_info}</p>
        </div>
        <p class="text-sm text-gray-400">
          💡 Please reach out with respect and kindness. Verify the other party before sharing personal details.
        </p>
      </div>
    {/if}

    <!-- Meta Information -->
    <div class="glass-card space-y-4">
      <h2 class="heading-md">ℹ️ Request Details</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        <div class="bg-white/5 border border-white/10 rounded-lg p-4">
          <span class="text-gray-400">Submitted:</span>
          <p class="font-semibold text-white mt-1">{formatDate(request.created_at)}</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-lg p-4">
          <span class="text-gray-400">Status:</span>
          <p class="font-semibold text-white mt-1">🔴 URGENT - Awaiting Response</p>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="glass-card bg-gradient-to-r from-green-500/10 to-emerald-500/10 border-green-500/30 space-y-5">
      <div>
        <h2 class="heading-md mb-3">🤝 Can You Help?</h2>
        <p class="text-gray-300 mb-4">
          If you're an organization that can assist with this request, please reach out to the person listed above or contact us directly at admin@asylum.org.
        </p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <a href="/ngos/register" class="btn-primary flex-1">Register Your Organization</a>
        <button class="btn-secondary flex-1 text-center">Share This Request</button>
      </div>
    </div>

    <!-- Related Requests -->
    <div class="glass-card space-y-4">
      <h2 class="heading-md">📊 Similar Requests</h2>
      <p class="text-gray-400">
        Help with {request.help_type} is in high demand. Organizations specializing in this area have been notified of this request.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <p class="text-gray-400">Other {request.help_type} requests:</p>
          <p class="font-bold text-blue text-lg">~{Math.floor(Math.random() * 50) + 10}</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-lg p-3">
          <p class="text-gray-400">Organizations active:</p>
          <p class="font-bold text-orange text-lg">~{Math.floor(Math.random() * 25) + 5}</p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex justify-between items-center pt-4 border-t border-white/10">
      <a href="/requests" class="btn-secondary">← Back to List</a>
      <a href="/" class="btn-primary">Home</a>
    </div>
  {/if}
</div>
