\clearpage

\begin{center}
\textbf{\Large <STIMTAG_A> (<REGION_A>), <PULSE_FREQ_A> Hz, <AMPLITUDE_A> mA , Session(s): <SESSIONS>}
\textbf{\Large <STIMTAG_B> (<REGION_B>), <PULSE_FREQ_B> Hz, <AMPLITUDE_B> mA , Session(s): <SESSIONS>}
\end{center}

\begin{table}[!h]
\centering
\begin{tabular}{c|c|c|c}
\multicolumn{4}{c}{\textbf{Free Recall}} \\
\hline
$<N_WORDS>$ words & $<N_CORRECT_WORDS>$ correct ($<PC_CORRECT_WORDS>$\%) &$<N_PLI>$ PLI ($<PC_PLI>$\%) &$<N_ELI>$ ELI ($<PC_ELI>$\%) \\ \hline
\end{tabular}
\caption{An intrusion was a word that was vocalized during the retrieval period that was not studied on the most recent list. Intrusions were either words from a previous list (\textbf{PLI}: prior-list intrusions) or words that were not studied at all (\textbf{ELI}: extra-list intrusions).}
\end{table}

\begin{table}[!h]
\centering
\begin{tabular}{c|c|c}
\multicolumn{3}{c}{\textbf{Math distractor}} \\
\hline
$<N_MATH>$ math problems & $<N_CORRECT_MATH>$ correct ($<PC_CORRECT_MATH>$\%) & $<MATH_PER_LIST>$ problems per list  \\ \hline
\end{tabular}
\caption{After each list, the patient was given 20 seconds to perform as many arithmetic problems as possible, which served as a distractor before the beginning of recall.}
\end{table}

\begin{figure}[!h]
\centering
\textbf{Probability of Recall}
\includegraphics[scale=0.4]{<PROB_RECALL_PLOT_FILE>}
\caption{\textbf{Free recall:}
(a) Overall probability of recall as a function of serial position.
(b) Probability of first recall as a function of serial position.}
\end{figure}

\begin{table}[!h]
\centering
\begin{tabular}{c|c|c|c|c}
\multicolumn{5}{c}{\textbf{Stim vs <COMPARISON_LIST_TYPE> Recalls}} \\
\hline
A & $<N_CORRECT_STIM_A>/<N_TOTAL_STIM_A>$ ($<PC_FROM_STIM_A>$\%) from stim lists & $<N_CORRECT_NONSTIM_A>/<N_TOTAL_NONSTIM_A>$ ($<PC_FROM_NONSTIM_A>$\%) from <COMPARISON_LIST_TYPE> lists & $\chi^2(1)=<CHISQR_A>$ & $p=<PVALUE_A>$ \\
B & $<N_CORRECT_STIM_B>/<N_TOTAL_STIM_B>$ ($<PC_FROM_STIM_B>$\%) from stim lists & $<N_CORRECT_NONSTIM_B>/<N_TOTAL_NONSTIM_B>$ ($<PC_FROM_NONSTIM_B>$\%) from <COMPARISON_LIST_TYPE> lists & $\chi^2(1)=<CHISQR_B>$ & $p=<PVALUE_B>$ \\
A+B & $<N_CORRECT_STIM_AB>/<N_TOTAL_STIM_AB>$ ($<PC_FROM_STIM_AB>$\%) from stim lists & $<N_CORRECT_NONSTIM_AB>/<N_TOTAL_NONSTIM_AB>$ ($<PC_FROM_NONSTIM_AB>$\%) from <COMPARISON_LIST_TYPE> lists & $\chi^2(1)=<CHISQR_AB>$ & $p=<PVALUE_AB>$ \\
\hline
<ITEMLEVEL_COMPARISON>
\end{tabular}
\end{table}

\begin{table}[!h]
\centering
\begin{tabular}{c|c|c}
\multicolumn{3}{c}{\textbf{Stim vs  <COMPARISON_LIST_TYPE> Intrusions}} \\
\hline
A & $<N_STIM_INTR_A>/<N_TOTAL_STIM_A>$ ($<PC_FROM_STIM_INTR_A>$\%) from stim lists & $<N_NONSTIM_INTR_A>/<N_TOTAL_NONSTIM_A>$ ($<PC_FROM_NONSTIM_INTR_A>$\%) from <COMPARISON_LIST_TYPE> lists \\
B & $<N_STIM_INTR_B>/<N_TOTAL_STIM_B>$ ($<PC_FROM_STIM_INTR_B>$\%) from stim lists & $<N_NONSTIM_INTR_B>/<N_TOTAL_NONSTIM_B>$ ($<PC_FROM_NONSTIM_INTR_B>$\%) from <COMPARISON_LIST_TYPE> lists \\
A+B & $<N_STIM_INTR_AB>/<N_TOTAL_STIM_AB>$ ($<PC_FROM_STIM_INTR_AB>$\%) from stim lists & $<N_NONSTIM_INTR_AB>/<N_TOTAL_NONSTIM_AB>$ ($<PC_FROM_NONSTIM_INTR_AB>$\%) from <COMPARISON_LIST_TYPE> lists \\
\hline
\end{tabular}
\end{table}
\clearpage

\begin{center}
\textbf{\Large Stim and recall analysis}
\end{center}

\begin{figure}[!h]
    \begin{subfigure}[b]{.45\textwidth}
        \includegraphics[height=0.25\textheight]{<STIM_AND_RECALL_PLOT_FILE_A>}
    \end{subfigure}\hfill
    \begin{subfigure}[b]{.45\textwidth}
         \includegraphics[height=0.25\textheight]{<STIM_AND_RECALL_PLOT_FILE_B>}
    \end{subfigure}\hfill
\end{figure}
\begin{figure}[!h]
    \begin{subfigure}[b]{.45\textwidth}
        \includegraphics[height=0.25\textheight]{<STIM_AND_RECALL_PLOT_FILE_AB>}
    \end{subfigure}\hfill
    \begin{subfigure}[b]{.45\textwidth}
         \includegraphics[height=0.25\textheight]{<STIM_AND_RECALL_PLOT_FILE_NOSTIM>}
    \end{subfigure}\hfill
    \caption*{\textbf{Stim and recall:} Number of stims and recalled items per list.
              Red circles represent the number of recalled items from stim lists.
              Blue circles represent the number of recalled items from non-stim lists.
              Grey circles represent the number of recalled items from parameter search lists.
              Bars represent the number of stims per list.}
\end{figure}

\begin{figure}[!h]
    \begin{subfigure}[b]{.30\textwidth}
        \includegraphics[scale=0.3]{<PROB_STIM_PLOT_FILE_A>}
    \end{subfigure}\hfill
    \begin{subfigure}[b]{.30\textwidth}
        \includegraphics[scale=0.3]{<PROB_STIM_PLOT_FILE_B>}
    \end{subfigure}\hfill
    \begin{subfigure}[b]{.30\textwidth}
         \includegraphics[scale=0.3]{<PROB_STIM_PLOT_FILE_AB>}
    \end{subfigure}\hfill
    \caption*{Probability of stimulation as a function of serial position.}
\end{figure}

<BIOMARKER_PLOTS>



