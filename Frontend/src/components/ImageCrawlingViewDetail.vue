<template>
  <b-modal ref="modalViewDetail" title="이미지 상세 정보">
    <!-- 이미지 상세 정보를 표시할 내용 추가 -->
    <div>
      <b-img :src="imageInfo.imageURL" alt="이미지 설명" fluid />
      <p>이미지 작성자: {{ imageInfo.user }}</p>
      <p>이미지 타입: {{ imageInfo.type }}</p>
      <p>이미지 태그: {{ imageInfo.tags }}</p>
      <p>이미지 키워드: {{ imageInfo.keyword }}</p>
      <p>이미지 카테고리: {{ imageInfo.category_id }}</p>
      <p>이미지 높이: {{ imageInfo.imageHeight }}</p>
      <p>이미지 넓이: {{ imageInfo.imageWidth }}</p>
      <p>이미지 생성일: {{ imageInfo.created_at }}</p>
    </div>
  </b-modal>
</template>

<script>
export default {
  props: {
    imageInfo: Object // 부모 컴포넌트에서 전달된 이미지 정보를 받습니다.
  },
  methods: {
    open(image) {
      // 모달 창을 열 때 이미지 정보를 설정합니다.
      this.imageInfo = image;
      this.$refs.modalViewDetail.show();
    }
  }
};
</script>