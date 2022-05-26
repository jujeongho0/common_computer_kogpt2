import torch
from tokenizers import SentencePieceBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel
import streamlit as st
from streamlit_chat import message
import tokenizers

st.header("fine-tuned kogpt2를 이용한 챗봇")

@st.cache(hash_funcs={tokenizers.Tokenizer: lambda _: None, tokenizers.AddedToken: lambda _: None})
def load():
    tokenizer = SentencePieceBPETokenizer("vocab.json", "merges.txt")
    tokenizer.add_special_tokens(['<s>', '</s>'])
    tokenizer.no_padding()
    tokenizer.no_truncation()

    config = GPT2Config(vocab_size=50000)
    model = GPT2LMHeadModel(config)
    model_dir = 'my_model.bin'
    model.load_state_dict(torch.load(model_dir, map_location=torch.device('cpu')), strict=False)

    return model, tokenizer


model, tokenizer = load()

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

utter = st.text_input("당신: ", key="input")

if utter:
    encoded_utter = torch.tensor(tokenizer.encode('<s>' + utter + '</s><s>').ids).unsqueeze(0)

    sample_output = model.generate(
        encoded_utter,
        num_return_sequences=1,
        do_sample=True,
        max_length=128,
        top_k=50,
        top_p=0.95,
        eos_token_id=tokenizer.token_to_id('</s>'),
        early_stopping=True,
        bad_words_ids=[[tokenizer.token_to_id('<unk>')]]
    )

    decoded_output = tokenizer.decode_batch(sample_output.tolist())[0]

    answer = decoded_output.replace(utter, '').lstrip(' ')

    st.session_state.past.append(utter)
    st.session_state.generated.append(answer)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')