def consolidate_bias_results(text, bias_detections):
    """
    Consolidates bias detection by calculating some metrics:
    - Total bias confidence score
    - Total number of excerpts detected
    - Types of bias detected
    - Bias confidence score for each type of bias
    - Number of excerpt detections for each type of bias
    - Excerpts, spans, and reformulated excerpts for each type of bias
    - Neutrality score by calculating the number of excerpts vs the total number of sentences in the article
    - Skips detections where bias_type is "unknown".
    """
    # Remove detections with bias_type "unknown"
    bias_detections = [d for d in bias_detections if getattr(d, "bias_type", None) != "unknown"]
    total_confidence = 0.0
    total_excerpts = 0
    bias_types = set()
    bias_confidences = {}
    bias_excerpts_count = {}
    bias_excerpts = {}

    for detection in bias_detections:
        bias_type = detection.bias_type
        confidence = detection.confidence
        excerpts = detection.excerpts

        total_confidence += confidence
        total_excerpts += len(excerpts)
        bias_types.add(bias_type)

        if bias_type not in bias_confidences:
            bias_confidences[bias_type] = 0.0
            bias_excerpts_count[bias_type] = 0

        bias_confidences[bias_type] += confidence
        bias_excerpts_count[bias_type] += len(excerpts)

        if bias_type not in bias_excerpts:
            bias_excerpts[bias_type] = {
                "excerpts": [],
                "spans": [],
                "reformulated_excerpts": []
            }

        bias_excerpts[bias_type]["excerpts"].extend(excerpts)
        bias_excerpts[bias_type]["spans"].extend(detection.spans)
        bias_excerpts[bias_type]["reformulated_excerpts"].extend(detection.reformulated_excerpts)

    sentences = text.split('.')
    total_sentences = len(sentences)
    neutrality_score = 1.0 - (total_excerpts / total_sentences) if total_sentences > 0 else 1.0

    average_confidence = total_confidence / len(bias_detections) if bias_detections else 0.0

    return {
        "average_confidence": average_confidence,
        "total_excerpts": total_excerpts,
        "bias_types": list(bias_types),
        "bias_confidences": bias_confidences,
        "bias_excerpts_count": bias_excerpts_count,
        "bias_excerpts": bias_excerpts,
        "neutrality_score": neutrality_score
    }
    