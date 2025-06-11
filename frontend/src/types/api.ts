// frontend/src/types/api.ts

// User Schemas (from backend/app/schemas/user.py UserOut)
export interface UserOut {
  id: number;
  username: string;
  email: string;
  is_educator: boolean;
  is_active: boolean;
  created_at: string; // ISO 8601 string for datetime
  updated_at: string | null;
}

// Lesson Schemas (from backend/app/schemas/lesson.py LessonOut)
export interface LessonOut {
  id: number;
  course_id: number;
  title: string;
  content_type: 'text' | 'video' | 'quiz' | 'link';
  content_url: string | null;
  text_content: string | null;
  order: number;
  created_at: string;
  updated_at: string | null;
  quizzes?: QuizOut[]; // Optional: Nested quizzes (summary)
  // Add a `course` property if the backend relation is loaded and desired here
  course?: CourseOut; // For Student Dashboard to link back to course
}

// Quiz Schemas (from backend/app/schemas/quiz.py QuizOut)
export interface QuizOut {
  id: number;
  lesson_id: number;
  title: string;
  description: string | null;
  created_at: string;
  updated_at: string | null;
  questions?: QuestionOut[]; // Optional: Nested questions (summary)
}

// Question Schemas (from backend/app/schemas/question.py QuestionOut)
export interface QuestionOut {
  id: number;
  quiz_id: number;
  question_text: string;
  question_type: 'MCQ' | 'TrueFalse' | 'ShortAnswer';
  created_at: string;
  updated_at: string | null;
  options?: OptionOut[]; // Optional: Nested options (summary)
}

// Option Schemas (from backend/app/schemas/option.py OptionOut)
export interface OptionOut {
  id: number;
  question_id: number;
  option_text: string;
  created_at: string;
  updated_at: string | null;
  // is_correct is NOT included for student view
}

// Course Schemas (from backend/app/schemas/course.py CourseOut)
export interface CourseOut {
  id: number;
  title: string;
  description: string | null;
  educator_id: number;
  created_at: string;
  updated_at: string | null;
  lessons?: LessonOut[]; // Optional: Nested lessons (summary)
}

// User Progress Schemas (from backend/app/schemas/user_progress.py UserProgressOut)
export interface UserProgressOut {
  id: number;
  user_id: number;
  lesson_id: number;
  is_completed: boolean;
  completed_at: string | null;
  last_accessed_at: string;
  lesson?: LessonOut; // Optional: Nested lesson details (to get lesson title, course info)
}

// User Answer Schemas (from backend/app/schemas/user_answer.py UserAnswerOut)
export interface UserAnswerOut {
    id: number;
    user_id: number;
    question_id: number;
    selected_option_id: number | null;
    user_answer_text: string | null;
    is_correct: boolean | null;
    answered_at: string;
}