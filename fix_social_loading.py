import re

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "r") as f:
    c = f.read()

target = """        conversationJob = viewModelScope.launch {
            repo.getConversations().collect { convs ->
                _conversations.value = convs
                _isLoading.value = false
            }
        }"""
        
replacement = """        conversationJob = viewModelScope.launch {
            kotlinx.coroutines.delay(1000)
            _isLoading.value = false
        }
        viewModelScope.launch {
            repo.getConversations().collect { convs ->
                _conversations.value = convs
                _isLoading.value = false
            }
        }"""
        
c = c.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "w") as f:
    f.write(c)

