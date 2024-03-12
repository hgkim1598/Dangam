<template>
  <div>
    <div v-if="imageInfo">
      <!-- 이미지 표시 -->
      <img :src="imageInfo.created_url" alt="Image" style="max-width: 100%; max-height: 400px;">

      <!-- 다른 상세 정보들 -->
      <div>
        <!-- 이미지 URL -->
        <p class="long-text"><strong>Image URL:</strong> {{ imageInfo.created_url }}</p>

        <!-- 다른 상세 정보들 -->
        <p><strong>프롬프트:</strong> {{ imageInfo.prompt }}</p>
        <p><strong>카테고리:</strong> {{ getCategoryName(imageInfo.category_id) }}</p>
        <!-- 필요한 다른 상세 정보들을 표시 -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['itemId'], // 부모 컴포넌트에서 전달된 itemId prop을 받음
  data() {
    return {
      imageInfo: null, // 이미지의 상세 정보를 저장할 객체
      categories: [] // 카테고리를 저장할 배열
    };
  },
  created() {
    // 컴포넌트가 생성될 때, itemId를 사용하여 API 호출
    this.fetchImageInfo();
    this.fetchCategories(); // 카테고리 데이터를 가져옴
  },

  methods: {
    async fetchImageInfo() {
      try {
        // 이미지의 상세 정보를 가져오는 API 요청을 보냄
        const response = await axios.get(`http://192.168.0.149:8000/create_image/${this.itemId}`);
        this.imageInfo = response.data; // 가져온 상세 정보를 imageInfo에 저장
        console.log(this.imageInfo);
      } catch (error) {
        console.error('Error fetching detailed information:', error);
        // 에러 처리
      }
    },

    async fetchCategories() {
      try {
        const apiUrl = 'http://192.168.0.149:8000/pixabay/image_categories/';
        const response = await axios.get(apiUrl);
        // 카테고리 배열에 데이터 저장
        this.categories = response.data;
        console.log(this.categories);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.id === categoryId);
      return category ? category.category : 'Unknown';
    }
  }
};
</script>

<style scoped>

.long-text {
  word-wrap: break-word; /* 긴 텍스트를 강제로 줄바꿈 */
  white-space: pre-wrap; /* 줄 바꿈과 함께 공백 유지 */
  overflow: visible; /* 넘치는 텍스트를 보이게 함 */
  display: block; /* 텍스트가 줄 바꿈되도록 설정 */
}
</style>