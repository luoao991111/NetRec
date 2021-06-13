import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    login: !!localStorage.getItem('authorization'),
    userId: localStorage.getItem('userId'),
    userName: localStorage.getItem('username'),
    authorization: localStorage.getItem('authorization') ? localStorage.getItem('authorization') : ''
  },
  mutations: {
    changeLogin (state, user) {
      state.authorization = user.authorization
      localStorage.setItem('authorization', user.authorization)
      localStorage.setItem('username', user.userName)
      localStorage.setItem('userId', user.userId)
      state.login = true
      state.userId = user.userId
      state.userName = user.userName
    },
    logout (state) {
      state.authorization = ""
      state.login = false
      state.userId = ""
      state.userName = ""
      localStorage.removeItem('authorization')
      localStorage.removeItem('username')
      localStorage.removeItem('userId')
    }
  },
  actions: {
  },
  modules: {
  }
})
