<script lang="ts">
	import { toasts, dismissToast } from '$lib/toast';
</script>

{#if $toasts.length > 0}
	<div class="toast-container">
		{#each $toasts as t (t.id)}
			<div class="toast {t.type}">
				<span>{t.message}</span>
				<button class="dismiss" onclick={() => dismissToast(t.id)} aria-label="Dismiss">
					<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
				</button>
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
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.7rem 0.75rem 0.7rem 1.1rem;
		border-radius: var(--radius);
		font-size: 0.875rem;
		font-weight: 500;
		box-shadow: var(--shadow);
		animation: slide-in 0.2s ease-out;
	}

	.toast.success {
		background: var(--color-tint-avail);
		color: var(--color-ink-avail);
	}

	.toast.error {
		background: var(--color-tint-danger);
		color: var(--color-ink-danger);
	}

	.toast.info {
		background: var(--color-tint-spot);
		color: var(--color-ink-spot);
	}

	.dismiss {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 22px;
		height: 22px;
		padding: 0;
		border: none;
		background: transparent;
		color: currentColor;
		opacity: 0.55;
	}

	.dismiss:hover {
		opacity: 1;
		background: rgba(0, 0, 0, 0.06);
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
