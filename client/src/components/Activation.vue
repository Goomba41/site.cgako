<template>

    <div class="container-fluid login-theme fill-height">

        <div class="row justify-content-center align-items-center h-100">
            <div class="form-box col col-xs-12 col-sm-8 col-md-4 col-lg-4 p-3 shaded">

                <div class="row justify-content-center align-items-center text-center mx-auto p-3">
                    <div class="col mx-auto">
                        <img src="../assets/logo-2.png" alt="ЦГАКО" width=250>
                        <h3 class="text-primary-color mt-4 small weight-100">
                          Панель управления сайтом ЦГАКО
                        </h3>
                        <h3 class="text-primary-color mb-4 small">
                          Подтверждение электронной почты
                        </h3>
                    </div>
                </div>

                <div class="row justify-content-center align-items-center text-center mx-auto p-3">
                    <b-alert :variant="msgType" show class="w-100">{{msgText}}</b-alert>
                </div>

                <div v-if="msgType==='success'"
                class="row justify-content-start align-items-start mx-auto p-3">
                    <b-button type="button" block :to="{ name: 'Login' }"
                    variant="primary" title="Перейти на страницу входа">
                      Перейти на страницу входа
                    </b-button>
                </div>

            </div>
        </div>

    </div>

</template>

<script>
import { EventBus } from '@/utils';

export default {
  name: 'Activation',
  data() {
    return {
      msgText: '',
      msgType: '',
    };
  },
  methods: {
  },
  props: ['token'],
  beforeMount() {
    this.$store.dispatch('verifyMail', this.token);
  },
  mounted() {
    EventBus.$on('messageActivation', (msg) => {
      this.msgText = msg.text;
      this.msgType = msg.type;
    });
  },
  beforeDestroy() {
    EventBus.$off('messageActivation');
  },
};
</script>

<style>
   @import '../assets/style-admin.css';
</style>
