import argparse
from .core import load_image, get_face_encoding, calculate_similarity

def main():
    parser = argparse.ArgumentParser(
        description="Compare similarity between two face images",
        epilog="Example: face-compare image1.jpg image2.jpg"
    )
    parser.add_argument("image1", help="Path to first image")
    parser.add_argument("image2", help="Path to second image")
    parser.add_argument("-t", "--threshold", type=float, default=0.6,
                        help="Similarity threshold (default: 0.6)")
    
    args = parser.parse_args()
    
    try:
        # 处理图像1
        img1 = load_image(args.image1)
        encoding1 = get_face_encoding(img1)
        
        # 处理图像2
        img2 = load_image(args.image2)
        encoding2 = get_face_encoding(img2)
        
        # 计算相似度
        similarity = calculate_similarity(encoding1, encoding2)
        is_match = similarity >= args.threshold
        
        # 输出结果
        print(f"Similarity Score: {similarity:.2%}")
        print(f"Match Result: {'MATCH' if is_match else 'NO MATCH'} (Threshold: {args.threshold})")
        exit(0 if is_match else 1)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(2)