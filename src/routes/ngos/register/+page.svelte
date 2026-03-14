<script lang="ts">
  import { createNgo } from '$lib/api/client';
  
  let name = '';
  let services = 'housing, legal, medical, food';
  let location = '';
  let contact_info = '';
  let sending = false;
  let done = false;
  let error = '';

  async function submit() {
    sending = true;
    error = '';
    try {
      await createNgo({ name, services, location, contact_info });
      done = true;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to register';
    } finally {
      sending = false;
    }
  }
</script>

{#if done}
  <div class="space-y-6 max-w-2xl mx-auto">
    <div class="glass-card bg-gradient-to-r from-green-500/10 to-emerald-500/10 border-green-500/50 text-center py-12 animate-fade-in">
      <div class="text-5xl mb-4">✅</div>
      <h1 class="heading-md mb-2">Registration Successful!</h1>
      <p class="subtext mb-6">
        Your organization is now part of the ASYLUM network. Help requests will be shared with you automatically.
      </p>
      <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
        <a href="/ngos" class="btn-primary">View All Organizations</a>
        <a href="/" class="btn-secondary">Back to Home</a>
      </div>
    </div>

    <div class="glass-card space-y-4">
      <h2 class="heading-md">🚀 Getting Started</h2>
      <div class="space-y-3 text-gray-300">
        <div class="flex gap-3">
          <span class="text-blue text-lg flex-shrink-0">1️⃣</span>
          <span>Your organization profile is live and searchable</span>
        </div>
        <div class="flex gap-3">
          <span class="text-blue text-lg flex-shrink-0">2️⃣</span>
          <span>We'll match help requests to your services automatically</span>
        </div>
        <div class="flex gap-3">
          <span class="text-blue text-lg flex-shrink-0">3️⃣</span>
          <span>People in need will contact you directly</span>
        </div>
        <div class="flex gap-3">
          <span class="text-orange text-lg flex-shrink-0">🎯</span>
          <span>Make a real difference in your community</span>
        </div>
      </div>
    </div>
  </div>
{:else}
  <div class="max-w-2xl mx-auto">
    <div class="mb-8">
      <a href="/ngos" class="inline-flex items-center gap-2 text-blue hover:text-orange transition-colors font-semibold mb-4">
        ← Back to Organizations
      </a>
      <h1 class="heading-lg text-4xl mb-2">Register Your Organization</h1>
      <p class="subtext">Join the ASYLUM network and connect with people who need your help.</p>
    </div>

    <form on:submit|preventDefault={submit} class="glass-card space-y-6">
      <!-- Organization Name -->
      <div>
        <label for="name" class="block text-sm font-semibold text-gray-300 mb-2">Organization Name *</label>
        <input
          id="name"
          type="text"
          bind:value={name}
          required
          placeholder="e.g. Red Cross Berlin"
          class="input-base"
        />
      </div>

      <!-- Location -->
      <div>
        <label for="location" class="block text-sm font-semibold text-gray-300 mb-2">Primary Location / City *</label>
        <input
          id="location"
          type="text"
          bind:value={location}
          required
          placeholder="e.g. Berlin"
          class="input-base"
        />
      </div>

      <!-- Services -->
      <div>
        <label for="services" class="block text-sm font-semibold text-gray-300 mb-2">Services You Provide *</label>
        <textarea
          id="services"
          bind:value={services}
          required
          rows="3"
          placeholder="List your services separated by commas&#10;Examples: housing, legal, medical, food, mental health, refugee services, clothing, transportation"
          class="input-base resize-none"
        ></textarea>
        <p class="text-xs text-gray-400 mt-2">
          💡 Be specific! This helps us match requests accurately. Examples: Housing & Shelter, Medical Care, Legal Consultation, Food Distribution, Mental Health Support, etc.
        </p>
      </div>

      <!-- Contact Information -->
      <div>
        <label for="contact_info" class="block text-sm font-semibold text-gray-300 mb-2">Contact Email or Phone *</label>
        <input
          id="contact_info"
          type="text"
          bind:value={contact_info}
          required
          placeholder="your-contact@example.com or +49 30 1234 5678"
          class="input-base"
        />
        <p class="text-xs text-gray-400 mt-2">
          💡 People in need will use this to contact you directly.
        </p>
      </div>

      {#if error}
        <div class="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300 text-sm">
          ⚠️ {error}
        </div>
      {/if}

      <div class="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={sending}
          class="btn-primary flex-1 sm:flex-none"
        >
          {sending ? '⏳ Registering...' : '🚀 Register Organization'}
        </button>
        <a href="/ngos" class="btn-secondary flex-1 sm:flex-none text-center">Cancel</a>
      </div>
    </form>

    <!-- Information Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
      <div class="glass-card bg-blue/10 border-blue/50">
        <h3 class="heading-md mb-3 text-blue">💼 Why Join?</h3>
        <ul class="space-y-2 text-sm text-gray-300">
          <li>✓ Expand your reach to people in need</li>
          <li>✓ Automatic matching with relevant requests</li>
          <li>✓ Zero setup time or fees</li>
          <li>✓ Help your community effectively</li>
        </ul>
      </div>
      
      <div class="glass-card bg-orange/10 border-orange/50">
        <h3 class="heading-md mb-3 text-orange">🔒 Privacy & Security</h3>
        <ul class="space-y-2 text-sm text-gray-300">
          <li>✓ Verified organizations only</li>
          <li>✓ No hidden fees or contracts</li>
          <li>✓ Full control over your profile</li>
          <li>✓ Direct person-to-person contact</li>
        </ul>
      </div>
    </div>
  </div>
{/if}
