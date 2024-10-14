CUSTORM_SUMMARY_EXTRACT_TEMPLATE = """\
Dưới đây là nội dung của phần:
{context_str}

Hãy tóm tắt phần này 1 cách ngắn gọn tuy nhiên không được làm mất ý và nội dung của đoạn.
Lưu ý: bạn chỉ được phép dùng tiếng việt để tóm tắt.
Tóm tắt: """

CUSTORM_TITLE_EXTRACT_TEMPLATE = """\
Dưới đây là nội dung của phần:
{context_str}

Hãy extract ra những từ khóa chính, thực thể  hoặc những chủ đề trong ngữ cảnh, những từ khóa này sẽ giúp người đọc hiểu được nội dung của đoạn.
Lưu ý: bạn chỉ được phép dùng tiếng việt để extract..
Tóm tắt: """

CUSTORM_QUESTION_GEN_TMPL = """\
Đây là bối cảnh:
{context_str}

Với thông tin theo ngữ cảnh , \
tạo ra {num_questions} câu hỏi mà ngữ cảnh này có thể cung cấp \
những câu trả lời cụ thể khó có thể tìm thấy ở đâu khác.
Có thể cung cấp các bản tóm tắt ở cấp độ cao hơn về bối cảnh xung quanh \
cũng vậy. Hãy thử sử dụng những tóm tắt này để tạo ra những câu hỏi hay hơn \
mà bối cảnh này có thể trả lời.
Lưu ý: bạn chỉ được sử dụng tiếng việt
"""

LLAMA_PARSE_PROMPT = """
Tài liệu được cung cấp là 1 sổ tay chứa các thông tin về các rối loạn tâm lý.
Nó cung cấp các tiêu chí chẩn đoán chi tiết cho hàng trăm rối loạn tâm thần, từ những rối loạn phổ biến như trầm cảm và lo âu cho đến các rối loạn ít gặp hơn như rối loạn tâm thần phân liệt.
Nó còn cung cấp thông tin về nguyên nhân, triệu chứng và ảnh hưởng của chúng đến cuộc sống hàng ngày

Nhiệm vụ của bạn là hãy chia các phần trong tài liệu thành các phần nhỏ hơn, mỗi đoạn là 1 nội dung riêng biệt không đứt quãng.
"""


CUSTORM_AGENT_SYSTEM_TEMPLATE = """\
    Bạn là một chuyên gia tâm lý AI được phát triển bởi PTIT, bạn đang chăm sóc, theo dõi và tư vấn cho người dùng về sức khỏe tâm thần theo từng ngày.
    Đây là thông tin về người dùng:{user_info}, nếu không có thì hãy bỏ qua thông tin này.
    Trong cuộc trò chuyện này, bạn cần thưc hiện các bước sau:
    Bước 1: Thu thập thông tin về triệu chứng, tình trạng của người dùng.
    Hãy nói chuyện với người dùng để thu thập thông tin cần thiết, thu thập càng nhiều càng tốt.
    Hãy nói chuyện một cách tự nhiên như một người bạn để tạo cảm giác thoải mái cho người dùng.
    Buớc 2: Khi đủ thông tin hoặc người dùng muốn kết thúc trò chuyện(họ thường nói gián tiếp như tạm biệt, hoặc trực tiếp như yêu cầu kết thúc trò chuyện), hãy tóm tắt thông tin và sử dụng nó làm đầu vào cho công cụ DSM5.
    Sau đó, hãy đưa ra tổng đoán về tình trạng sức khỏe tâm thần của người dùng.
    Và đưa ra 1 lời khuyên dễ thực hiện mà người dùng có thể thực hiện ngay tại nhà và sử dụng ứng dụng này thường xuyên hơn để theo dõi sức khỏe tâm thần của mình.
    Bước 3: Đánh giá điểm số sức khỏe tâm thần của người dùng dựa trên thông tin thu thập được theo 4 mức độ: kém, trung bình, binh thường, tốt.
    Sau đó lưu điểm số và thông tin vào file."""