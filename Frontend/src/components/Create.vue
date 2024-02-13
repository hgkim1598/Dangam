<template>
    <b-form @submit.prevent="submitForm" no-ok no-cancel>
      <b-form-group label="카테고리">
        <b-form-select v-model="category" :options="categories"></b-form-select>
      </b-form-group>
      <b-form-group label="사자성어(한국어) *" label-for="contentsKr">
        <b-form-input id="contentsKr" v-model="contentsKr" required></b-form-input>
      </b-form-group>
      <b-form-group label="사자성어(한문)" label-for="contentsZh">
        <b-form-input id="contentsZh" v-model="contentsZh"></b-form-input>
      </b-form-group>
      <b-form-group label="뜻 풀이 *" label-for="contentsDetail">
        <b-form-input id="contentsDetail" v-model="contentsDetail" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">{{ isUpdateMode ? '수정' : '등록' }}</b-button>
    </b-form>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: ['isEditMode', 'editId'], // 수정 모드 여부 및 수정할 아이템의 ID props
    data() {
      return {
        category: null,
        categories: ['편지', '기타', '욕심'],
        contentsDetail: '',
        contentsKr: '',
        contentsZh: '',
        isUpdateMode: false // 수정 모드 여부
      };
    },
    created() {
      // 수정 모드인 경우, 데이터를 불러와서 폼에 채움
      if (this.isEditMode) {
        this.isUpdateMode = true;
        this.fetchData(this.editId); // 수정할 아이템의 ID로 데이터를 가져옴
      }
    },
    methods: {
      async fetchData(id) {
        try {
          const response = await axios.get(`http://192.168.0.149:8000/fourchar/${id}`);
          const data = response.data;
          // 가져온 데이터를 각 input 필드에 설정
          this.category = data.category;
          this.contentsKr = data.contents_kr;
          this.contentsZh = data.contents_zh;
          this.contentsDetail = data.contents_detail;
        } catch (error) {
          console.error('데이터를 불러오는 중 오류 발생:', error);
        }
      },
      async submitForm() {
        const data = {
          contents_kr: this.contentsKr,
          contents_zh: this.contentsZh,
          contents_detail: this.contentsDetail,
          category: this.category
        };
  
        try {
          if (this.isUpdateMode) {
            await axios.put(`http://192.168.0.149:8000/fourchar/edit/${this.editId}`, data);
            console.log('데이터 수정 성공');
          } else {
            await axios.post('http://192.168.0.149:8000/fourchar/new', data);
            console.log('데이터 등록 성공');
          }
        } catch (error) {
          console.error(this.isUpdateMode ? '데이터 수정 실패' : '데이터 등록 실패', error);
        }
      }
    }
  };
  </script>