<script lang="ts">
	import { toasts } from '$lib/toast';
</script>

{#if $toasts.length > 0}
	<div class="toast-container">
		{#each $toasts as t (t.id)}
			<div class="toast {t.type}">
				{t.message}
			</div>
		{/each}
	</div>
{/if}

<style>
	.toast-container {
		position: fixed;
		top: 1rem;
		right: 1rem;
		z-index: 1000;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.toast {
		padding: 0.75rem 1.25rem;
		border-radius: var(--radius);
		font-size: 0.875rem;
		font-weight: 500;
		box-shadow: var(--shadow);
		animation: slide-in 0.2s ease-out;
	}

	.toast.success {
		background: var(--color-badge-available);
		color: var(--color-badge-available-text);
		border: 1px solid var(--color-success);
	}

	.toast.error {
		background: #f1ddd7;
		color: var(--color-danger);
		border: 1px solid var(--color-danger);
	}

	.toast.info {
		background: #dbe9e9;
		color: var(--color-accent);
		border: 1px solid var(--color-accent);
	}

	@keyframes slide-in {
		from {
			transform: translateX(100%);
			opacity: 0;
		}
		to {
			transform: translateX(0);
			opacity: 1;
		}
	}
</style>
