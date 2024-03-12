<template>
  <b-modal ref="modalViewDetail" title="이미지 상세 정보">
    <!-- 이미지 상세 정보를 표시할 내용 추가 -->
    <div>
      <b-img :src="imageInfo.imageURL" alt="이미지 설명" fluid />
      <p><strong>이미지 작성자:</strong> {{ imageInfo.user }}</p>
      <p><strong>이미지 타입:</strong> {{ imageInfo.type }}</p>
      <p><strong>이미지 태그:</strong> {{ imageInfo.tags }}</p>
      <p><strong>이미지 키워드:</strong> {{ imageInfo.keyword }}</p>
      <p><strong>이미지 카테고리:</strong> {{ imageInfo.category_id }}</p>
      <p><strong>이미지 높이:</strong> {{ imageInfo.imageHeight }}</p>
      <p><strong>이미지 넓이:</strong> {{ imageInfo.imageWidth }}</p>
      <p><strong>이미지 생성일:</strong> {{ imageInfo.created_at }}</p>
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