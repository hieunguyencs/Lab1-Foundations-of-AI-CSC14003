# Cài đặt

## BẢN ĐỒ BÌNH THƯỜNG (7đ)
- 5 cái 
- Cài thuật:
    + 3 thuật ko thông tin: **DFS**, **BFS**, **UCS**
    + 2 thuật có thông tin (tự định nghĩa ít nhất 2 hàm heuristic, mỗi thuật chạy 2 hàm này): **Greedy Best First Search**, **A***


## BẢN ĐỒ ĐIỂM THƯỞNG (2đ)
- Các điểm thưởng khi đi qua được giảm chi phí, giá trị < 0, có thể khác nhau 
- 3 cái (2, 5, 10 điểm thưởng) 
- Ko bắt buộc đi qua hết điểm thưởng
- Đề xuất 1 thuật để tối ưu chi phí (nếu ko tối ưu được thì cài heuristic để tham lam).

## BẢN ĐỒ ĐIỂM ĐÓN (1đ)
- Điểm đón là điểm bắt buộc phải đi qua trước khi đi tới điểm exit
- 3 cái (5, 10, 25 điểm đón)
- Đề xuất 1 thuật để tối ưu chi phí (nếu ko tối ưu được thì cài heuristic để tham lam).

## BẢN ĐỒ DỊCH CHUYỂN TỨC THỜI (1đ cộng)
- Thêm 1 vài điểm dịch chuyển ( Điểm (i,j) có thêm khả năng dịch chuyển tới (i',j') )
- 3 cái
- Đề xuất 1 thuật để tối ưu chi phí (nếu ko tối ưu được thì cài heuristic để tham lam).

## Lưu ý 
- Mỗi loại bản đồ: ít nhất 1 bản đồ dài hơn 35 và 1 bản đồ rộng hơn 15
- Simulate quá trình tìm đường đi thay vì chỉ vẽ ra đường đi (vd: https://www.youtube.com/watch?v=Gk4Dga5m1QQ): +0.5đ


# Báo cáo
## BẢN ĐỒ BÌNH THƯỜNG:
- Chạy trên 5 thuật trên 5 bản đồ và so sánh 5 thuật dựa trên: 
    + Tính đầy đủ
    + Tính tối ưu 
    + Độ mở các nút 
    + Thời gian chạy
    + Đối với mỗi hàm heuristic, so sánh sự khác nhau giữa các thuật khi chạy hàm heuristic đó
 - Mỗi thuật 1 hình mình họa

## Bản đồ điểm đón và bản đồ điểm thưởng
- Đề xuất thuật toán
- Hình minh họa
