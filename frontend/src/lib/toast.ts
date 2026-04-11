import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'info';

interface ToastMessage {
	id: number;
	message: string;
	type: ToastType;
}

let nextId = 0;

export const toasts = writable<ToastMessage[]>([]);

export function toast(message: string, type: ToastType = 'info', duration = 3000) {
	const id = nextId++;
	toasts.update((t) => [...t, { id, message, type }]);
	setTimeout(() => {
		toasts.update((t) => t.filter((m) => m.id !== id));
	}, duration);
}
