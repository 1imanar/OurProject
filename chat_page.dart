import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();
  final List<Content> _chatHistory = [];
  late final ChatSession _chatSession;
  late final GenerativeModel _model;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _model = GenerativeModel(
      model: 'gemini-1.5-flash',
      apiKey: 'AIzaSyCGXgXQJjNhgBIRL6ORZWI3cDnrHKCW1zw',
      systemInstruction: Content.system(
        'أنت مساعد ذكي لتطبيق سياحة جنوب السعودية. تجيب فقط عن عسير، نجران، جازان، والباحة. '
        'إذا سُئلت عن أي شيء خارج هذه المناطق، اعتذر بلباقة وقل أنك خبير في الجنوب فقط.',
      ),
    );
    _chatSession = _model.startChat();
  }

  Future<void> _sendChatMessage() async {
    if (_controller.text.isEmpty) return;

    final userText = _controller.text;

    setState(() {
      // إضافة رسالة المستخدم
      _chatHistory.add(Content.text(userText));
      _isLoading = true;
    });

    _controller.clear();

    try {
      // إرسال الرسالة إلى Gemini
      final response = await _chatSession.sendMessage(Content.text(userText));

      setState(() {
        // التعديل هنا: نأخذ النص الصافي من الرد ونضيفه للقائمة
        if (response.text != null) {
          _chatHistory.add(Content.model([TextPart(response.text!)]));
        }
      });
    } catch (e) {
      setState(() {
        _chatHistory.add(Content.model([TextPart('خطأ: $e')]));
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('مساعد الجنوب الذكي')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(15),
              itemCount: _chatHistory.length,
              itemBuilder: (context, index) {
                var content = _chatHistory[index];
                bool isUser = content.role == 'user';
                // تعديل هنا لعرض النص بشكل صحيح
                String messageText = content.parts
                    .whereType<TextPart>()
                    .map((e) => e.text)
                    .join();

                return Align(
                  alignment:
                      isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 5),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.green[100] : Colors.grey[200],
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: Text(messageText),
                  ),
                );
              },
            ),
          ),
          if (_isLoading) const LinearProgressIndicator(),
          Padding(
            padding: const EdgeInsets.all(10),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'اسألني عن الجنوب...',
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Colors.green),
                  onPressed: _sendChatMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
