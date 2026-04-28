function askAssistant() {
    let input = document.getElementById("userQuestion").value.toLowerCase();
    let reply = document.getElementById("assistantReply");

    if (input.includes("ابها")) {
        reply.innerHTML = "أفضل الأماكن في أبها: السودة، حديقة أبو خيال، قرية المفتاحة.";
    }
    else if (input.includes("الباحة")) {
        reply.innerHTML = "في الباحة: منتزه رغدان، غابة خيرة، قرية ذي عين.";
    }
    else if (input.includes("جازان")) {
        reply.innerHTML = "في جازان: الكورنيش، جزيرة فرسان، جبال فيفا.";
    }
    else if (input.includes("نجران")) {
        reply.innerHTML = "في نجران: الأخدود، قصر الإمارة، حبونا.";
    }
    else if (input.includes("كوفي")) {
        reply.innerHTML = "يوجد العديد من المقاهي الجميلة في جميع المناطق.";
    }
    else if (input.includes("مطعم")) {
        reply.innerHTML = "يوجد مطاعم مميزة في كل منطقة حسب اختيارك.";
    }
    else {
        reply.innerHTML = "عذرًا، حاول كتابة اسم منطقة مثل أبها أو الباحة.";
    }
}