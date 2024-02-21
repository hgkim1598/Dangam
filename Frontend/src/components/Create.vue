<template>
  <b-form @submit.prevent="submitForm" no-ok no-cancel>
    <b-form-group label="카테고리 *">
      <b-dropdown v-model="selectedCategory" :text="selectedCategory ? selectedCategory : '카테고리 선택'" variant="outline-primary" :class="{'invalid-dropdown': !selectedCategory}">
        <b-dropdown-menu class="custom-dropdown-menu">
          <div style="max-height: 300px; overflow-y: auto;">
            <b-form-radio v-for="(cat, index) in categories" :key="index" :value="cat" @input="selectedCategory = cat" name="category">
              {{ cat }}
            </b-form-radio>
          </div>
        </b-dropdown-menu>
      </b-dropdown>
    </b-form-group>
    <b-form-group label="사자성어(한국어) *" label-for="contentsKr">
      <b-form-input id="contentsKr" v-model="contentsKr" required></b-form-input>
    </b-form-group>
    <b-form-group label="사자성어(한문)" label-for="contentsZh">
      <b-form-input id="contentsZh" v-model="contentsZh"></b-form-input>
    </b-form-group>
    <b-form-group label="뜻 풀이 *" label-for="contentsDetail">
      <b-form-textarea id="contentsDetail" v-model="contentsDetail" required></b-form-textarea>
    </b-form-group>
    <b-button type="submit" variant="primary" :disabled="!selectedCategory || !contentsKr || !contentsDetail">{{ isUpdateMode ? '수정' : '등록' }}</b-button>
  </b-form>
</template>

<script>
import axios from 'axios';

export default {
  props: ['isEditMode', 'editId'], // 수정 모드 여부 및 수정할 아이템의 ID props
  data() {
    return {
      selectedCategory: null,
      categories: [], // 카테고리 리스트를 빈 배열로 초기화합니다.
      contentsDetail: '',
      contentsKr: '',
      contentsZh: '',
      isUpdateMode: false // 수정 모드 여부
    };
  },
  async created() {
    // 수정 모드인 경우, 데이터를 불러와서 폼에 채움
    if (this.isEditMode) {
      await this.fetchData(this.editId); // 수정할 아이템의 ID로 데이터를 가져옴
      this.isUpdateMode = true;
    } else {
      this.isUpdateMode = false; // 수정 모드가 아닌 경우에는 isUpdateMode를 false로 초기화
    }
    
    // 카테고리 리스트를 API에서 가져옵니다.
    await this.fetchCategories();
  },
  methods: {
    async fetchData(id) {
      try {
        const response = await axios.get(`http://192.168.0.149:8000/fourchar/${id}`);
        const data = response.data;
        // 가져온 데이터를 각 input 필드에 설정
        this.selectedCategory = data.category;
        this.contentsKr = data.contents_kr;
        this.contentsZh = data.contents_zh;
        this.contentsDetail = data.contents_detail;
      } catch (error) {
        console.error('데이터를 불러오는 중 오류 발생:', error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://192.168.0.149:8000/category/?select_category=fourchar');
        this.categories = response.data; // API에서 받아온 카테고리 리스트를 저장합니다.
      } catch (error) {
        console.error('카테고리를 불러오는 중 오류 발생:', error);
      }
    },
    async submitForm() {
      if (!this.selectedCategory || !this.contentsKr || !this.contentsDetail) {
        // 카테고리, 사자성어(한국어), 뜻 풀이 중 하나라도 입력되지 않은 경우
        alert('필수 입력 항목을 모두 작성하세요.');
        return;
      }
      
      const data = {
        contents_kr: this.contentsKr,
        contents_zh: this.contentsZh,
        contents_detail: this.contentsDetail,
        category: this.selectedCategory
      };

      try {
        if (this.isUpdateMode) {
          await axios.put(`http://192.168.0.149:8000/fourchar/edit/${this.editId}`, data);
          console.log('데이터 수정 성공');
        } else {
          await axios.post('http://192.168.0.149:8000/fourchar/new', data);
          console.log('데이터 등록 성공');
        }
        // 성공적으로 데이터를 수정 또는 등록한 후에 모달 창을 닫고 메인 페이지를 새로고침합니다.
        this.hideModal();
        location.reload(); // 현재 페이지를 새로 고침합니다.
      } catch (error) {
        console.error(this.isUpdateMode ? '데이터 수정 실패' : '데이터 등록 실패', error);
      }
    },
    hideModal() {
      this.$emit('closeModal'); // 부모 컴포넌트로 모달을 닫도록 이벤트 발생
    }
  }
};
</script>

<style>
.invalid-dropdown .btn-outline-primary {
  border-color: red;
}
</style>