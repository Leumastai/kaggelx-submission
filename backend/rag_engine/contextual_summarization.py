
from typing import *
from langchain.chains.llm import LLMChain
from langchain import HuggingFacePipeline
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.schema.retriever import Document



def summarization(
    llm: Union[HuggingFacePipeline, Any], query_docs: List[Document] = None, 
    runtype: str = "raw_text", key_words: Optional[str] = None,
    ) -> str:

    """
    ### Contextual summarization function. 
    This fuction trys to summarize a document, text, or webpage contextually from the user POV and keywords.
    Args:
        - llm: Union[HuggingFacePipeline, Any] = LLModel
        - query_docs: List[Document] = Document loaded with langchain 
                either from a document, webpage, or a raw text
        - runtype: str = can be `raw_text` for summarization on a webpage or raw text or 
                file` for summarization on a document.
        - keywords: Optional[str] = keywords from which the user want to summarize from.

    Retruns:
        - contextual_summary: str =  contextual summary of the query docs inputed using the given parameters
    """
    
    if runtype == 'raw_text':   # contextual summarization from a raw text

        prompt_template = """
            Using the following keywords context `{key_words}`,
            Write a context-based summary for the following text:
            "{text}"
            CONTEXT-BASED SUMMARY: """

        CONTEXTUAL_SUMMARY_PROMPT = PromptTemplate(
            input_variables=["key_words", "text"],
            template=prompt_template
        )
        llm_chain = LLMChain(llm=llm, prompt=CONTEXTUAL_SUMMARY_PROMPT)

        stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain, document_variable_name="text",
        )

        contextual_summary = stuff_chain.run({
            "input_documents":query_docs, 
            "key_words":key_words})

        return contextual_summary


    if runtype == 'file':   # contextual summarization from a large file
        
        assert query_docs != None
        
        # Map Chain
        # Based on the documents retrieved, summarized them into their inherent context.
        map_template = """The following is a set of documents
            {docs}
            Based on this list of docs, please identify the inherent context within it
            Context Based Summary: """
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        # Reduce Chain
        # Takes the summaries from `map_prompt` and distill them into on main consolidated summary
        reduce_template = """The following is set of summaries:
            {doc_summaries}
            Take these and distill it into a final, consolidated contextual-based summary of the main context. 
            Context Based Summary: """
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="doc_summaries"
        )

        # Combines and iteravely reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )


        # contextual_summary = reduce_documents_chain.run(query_docs)
        # return contextual_summary
        # use the aboe two lines, if you don'r wish to use the map reduce chain
        # again, the reduce document chain is as good as the using the it alongside
        # the map reduce chain. 
        
        # use the lines below, if you're not querying from a vectorDB; 
        # where you get the advantage of a similarity metrics

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )
        
        contextual_summary = map_reduce_chain.run(query_docs)
        return contextual_summary

if __name__ == "__main__":

    from langchain.document_loaders import WebBaseLoader
    url = "https://techcrunch.com/2023/10/14/deal-dive-general-catalyst-healthcare-system/"
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    contextual_summary = summarization(
        llm, query_docs = docs, key_words = "VC, HATCo initiative, Healthcare")
