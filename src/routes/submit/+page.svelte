<script lang="ts">
  import { createHelpRequest } from '$lib/api/client';
  let name = '';
  let location = '';
  let help_type = 'housing';
  let description = '';
  let language = 'English';
  let contact_info = '';
  let sending = false;
  let done = false;
  let error = '';

  async function submit() {
    sending = true;
    error = '';
    try {
      await createHelpRequest({
        name,
        location,
        help_type,
        description,
        language,
        contact_info: contact_info || undefined
      });
      done = true;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to submit';
    } finally {
      sending = false;
    }
  }
</script>

{#if done}
  <div class="space-y-6 max-w-2xl mx-auto">
    <div class="glass-card bg-gradient-to-r from-green-500/10 to-emerald-500/10 border-green-500/50 text-center py-12 animate-fade-in">
      <div class="text-5xl mb-4">✅</div>
      <h1 class="heading-md mb-2">Request Submitted Successfully</h1>
      <p class="subtext mb-6">
        Your help request has been received and shared with our network of organizations. You'll be contacted soon.
      </p>
      <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
        <a href="/" class="btn-primary">Back to Home</a>
        <a href="/requests" class="btn-secondary">View All Requests</a>
      </div>
    </div>
    <div class="glass-card">
      <h2 class="heading-md mb-4">What Happens Next?</h2>
      <ul class="space-y-3 text-gray-300">
        <li class="flex gap-3">
          <span class="text-blue flex-shrink-0">1️⃣</span>
          <span>Your request is shared with nearby NGOs immediately</span>
        </li>
        <li class="flex gap-3">
          <span class="text-blue flex-shrink-0">2️⃣</span>
          <span>Matching organizations review your needs</span>
        </li>
        <li class="flex gap-3">
          <span class="text-blue flex-shrink-0">3️⃣</span>
          <span>You'll receive contact from organizations that can help</span>
        </li>
        <li class="flex gap-3">
          <span class="text-orange flex-shrink-0">🎯</span>
          <span>Stay in touch - your information is safe with us</span>
        </li>
      </ul>
    </div>
  </div>
{:else}
  <div class="max-w-2xl mx-auto">
    <div class="mb-8">
      <h1 class="heading-lg text-4xl mb-2">Submit a Help Request</h1>
      <p class="subtext">Tell us what you need. Organizations in your area will be notified immediately.</p>
    </div>

    <form on:submit|preventDefault={submit} class="glass-card space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <!-- Name Field -->
        <div>
          <label for="name" class="block text-sm font-semibold text-gray-300 mb-2">Your Name *</label>
          <input
            id="name"
            type="text"
            bind:value={name}
            required
            placeholder="Your full name"
            class="input-base"
          />
        </div>

        <!-- Location Field -->
        <div>
          <label for="location" class="block text-sm font-semibold text-gray-300 mb-2">City/Location *</label>
          <input
            id="location"
            type="text"
            bind:value={location}
            required
            placeholder="e.g. Berlin"
            class="input-base"
          />
        </div>
      </div>

      <!-- Type of Help -->
      <div>
        <label for="help_type" class="block text-sm font-semibold text-gray-300 mb-2">Type of Help Needed *</label>
        <select bind:value={help_type} id="help_type" class="input-base">
          <option value="housing">🏠 Housing & Shelter</option>
          <option value="medical">🏥 Medical & Health</option>
          <option value="legal">⚖️ Legal Support</option>
          <option value="food">🍽️ Food & Supplies</option>
          <option value="other">❓ Other</option>
        </select>
      </div>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-semibold text-gray-300 mb-2">Description of Your Needs *</label>
        <textarea
          id="description"
          bind:value={description}
          required
          placeholder="Please tell us what help you need and why..."
          rows="5"
          class="input-base resize-none"
        ></textarea>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <!-- Language -->
        <div>
          <label for="language" class="block text-sm font-semibold text-gray-300 mb-2">Language</label>
          <input
            id="language"
            type="text"
            bind:value={language}
            placeholder="English"
            class="input-base"
          />
        </div>

        <!-- Contact Info -->
        <div>
          <label for="contact_info" class="block text-sm font-semibold text-gray-300 mb-2">Contact (Email/Phone)</label>
          <input
            id="contact_info"
            type="text"
            bind:value={contact_info}
            placeholder="how to reach you (optional)"
            class="input-base"
          />
        </div>
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
          {sending ? '⏳ Submitting...' : '📤 Submit Request'}
        </button>
        <a href="/" class="btn-secondary flex-1 sm:flex-none text-center">Cancel</a>
      </div>
    </form>

    <div class="glass-card mt-8 bg-blue/10 border-blue/50">
      <h3 class="heading-md mb-3 text-blue">💡 Privacy & Safety</h3>
      <p class="text-gray-300 text-sm">
        Your information is shared only with verified organizations that can help. We never sell your data.
        All communications are monitored to ensure your safety.
      </p>
    </div>
  </div>
{/if}
