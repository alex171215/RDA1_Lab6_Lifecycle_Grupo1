package com.paulrosero.laboratorio1

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

// Extensión para SavedStateHandle que proporciona un MutableStateFlow sincronizado
// con el Bundle interno de SavedStateHandle para resistir Process Death
fun <T> SavedStateHandle.getMutableStateFlow(key: String, initialValue: T): MutableStateFlow<T> {
    val initial = this.get<T>(key) ?: initialValue
    val internalStateFlow = MutableStateFlow(initial)
    return object : MutableStateFlow<T> by internalStateFlow {
        override var value: T
            get() = internalStateFlow.value
            set(v) {
                internalStateFlow.value = v
                this@getMutableStateFlow[key] = v
            }

        override suspend fun emit(v: T) {
            this@getMutableStateFlow[key] = v
            internalStateFlow.emit(v)
        }

        override fun compareAndSet(expect: T, update: T): Boolean {
            val success = internalStateFlow.compareAndSet(expect, update)
            if (success) {
                this@getMutableStateFlow[key] = update
            }
            return success
        }
    }
}

class CounterViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {
    // Usamos SavedStateHandle para que el valor sobreviva incluso a Process Death
    private val _count = savedStateHandle.getMutableStateFlow("counter_key", 0)
    val count = _count.asStateFlow()

    fun increment() {
        _count.value++
    }
}
