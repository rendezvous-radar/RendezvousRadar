import torch
from transformers.generation.logits_process import LogitsProcessor

class ConstrainLogitsProcessor(LogitsProcessor):
    def __init__(self, valid_sequences):
        self.valid_prefixes = self._generate_prefixes(valid_sequences)

    def _generate_prefixes(self, sequences):
        """Generate all valid prefixes from tokenized sequences."""
        prefixes = set()
        for seq in sequences:
            for i in range(1, len(seq) + 1):
                prefixes.add(tuple(seq[:i]))
        return prefixes
    
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        """Mask logits that don't match valid prefixes."""
        current_seq = tuple(input_ids[0].tolist())  # Current sequence
        
        # Find valid next token IDs based on prefixes
        valid_next_tokens = set()
        for prefix in self.valid_prefixes:
            if prefix[:len(current_seq)] == current_seq:
                valid_next_tokens.add(prefix[len(current_seq)])
        
        # Mask invalid tokens
        mask = torch.ones_like(scores, dtype=torch.bool)
        for token_id in valid_next_tokens:
            mask[0, token_id] = False
        
        # Ensure we don't mask all tokens; otherwise, the generation will fail
        if mask.all():
            # In case all tokens are masked, allow the top-k logits for the next token
            mask[0, torch.topk(scores[0], 5).indices] = False
        
        # Apply the mask, setting invalid logits to a very large negative value
        scores[mask] = -float("inf")
        
        return scores